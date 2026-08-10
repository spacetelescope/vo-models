"""Prototype: structural conformance check between XSD complexTypes and pydantic-xml models."""

import typing
from dataclasses import dataclass, field

import xmlschema
from xmlschema.validators import XsdAnyElement, XsdElement, XsdGroup

from pydantic_xml.model import XmlEntityInfo


@dataclass
class Particle:
    name: str
    min_occurs: int
    max_occurs: object  # int or None (unbounded)
    in_choice: bool
    choice_repeats: bool  # the enclosing choice itself has maxOccurs > 1


def walk_content(group, inherited_max=1, in_choice=False, choice_repeats=False, out=None):
    """Flatten an XSD content model into element particles with effective cardinality."""
    if out is None:
        out = []
    is_choice = getattr(group, "model", None) == "choice"
    grp_max = group.max_occurs  # None == unbounded
    grp_repeats = grp_max is None or grp_max > 1

    for item in group:
        if isinstance(item, XsdAnyElement):
            out.append(Particle("##any", item.min_occurs, item.max_occurs, is_choice or in_choice, False))
        elif isinstance(item, XsdElement):
            out.append(
                Particle(
                    item.name,
                    item.min_occurs,
                    item.max_occurs,
                    is_choice or in_choice,
                    (is_choice and grp_repeats) or choice_repeats,
                )
            )
        elif isinstance(item, XsdGroup):
            walk_content(
                item,
                in_choice=in_choice or is_choice,
                choice_repeats=choice_repeats or (is_choice and grp_repeats),
                out=out,
            )
    return out


def xsd_shape(ct):
    """Return (elements, attributes) descriptors for an XSD complexType."""
    elements = {}
    if ct.content is not None and isinstance(ct.content, XsdGroup):
        for p in walk_content(ct.content):
            local = p.name.split("}")[-1] if p.name else p.name
            # a repeating choice makes every branch effectively unbounded
            unbounded = p.max_occurs is None or (p.max_occurs or 0) > 1 or p.choice_repeats
            prev = elements.get(local)
            elements[local] = Particle(
                local,
                min(p.min_occurs, prev.min_occurs) if prev else p.min_occurs,
                None if unbounded else 1,
                p.in_choice,
                p.choice_repeats,
            )
    attributes = {
        name: attr.use == "required"
        for name, attr in ct.attributes.items()
    }
    return elements, attributes


def model_shape(cls):
    """Return (elements, attributes, text_fields) descriptors for a pydantic-xml model."""
    elements, attributes, text = {}, {}, []
    for fname, finfo in cls.model_fields.items():
        entity = next((m for m in finfo.metadata if isinstance(m, XmlEntityInfo)), None)
        ann = finfo.annotation
        is_list, is_opt = False, False
        origin = typing.get_origin(ann)
        if origin is typing.Union:
            args = [a for a in typing.get_args(ann) if a is not type(None)]
            is_opt = len(args) < len(typing.get_args(ann))
            ann = args[0] if args else ann
            origin = typing.get_origin(ann)
        if origin in (list, set, tuple):
            is_list = True
        loc = getattr(entity, "location", None)
        path = getattr(entity, "path", None) or fname
        ns = getattr(entity, "ns", None)
        # xsi:* attributes are schema-instance machinery, not declared in the complexType
        if ns == "xsi":
            continue
        rec = {"field": fname, "list": is_list, "optional": is_opt}
        if loc is not None and loc.name == "ATTRIBUTE":
            attributes[path] = rec
        elif loc is not None and loc.name == "ELEMENT":
            elements[path] = rec
        else:
            text.append(rec)
    return elements, attributes, text


def compare(type_name, ct, cls):
    """Yield human-readable findings."""
    xe, xa = xsd_shape(ct)
    me, ma, mt = model_shape(cls)
    findings = []

    for name, p in xe.items():
        if name == "##any":
            findings.append(f"  xs:any wildcard present in schema; model has no catch-all")
            continue
        m = me.get(name)
        if m is None:
            findings.append(f"  MISSING element <{name}>")
            continue
        unbounded = p.max_occurs is None
        if unbounded and not m["list"]:
            findings.append(f"  CARDINALITY <{name}>: schema allows many, model field '{m['field']}' is scalar")
        if not unbounded and m["list"]:
            findings.append(f"  CARDINALITY <{name}>: schema allows one, model field '{m['field']}' is a list")
        if p.min_occurs > 0 and m["optional"]:
            findings.append(f"  REQUIREDNESS <{name}>: schema requires it, model field '{m['field']}' is Optional")
    for name in me:
        if name not in xe:
            findings.append(f"  EXTRA element <{name}> in model, not in schema")

    for name, required in xa.items():
        m = ma.get(name)
        if m is None:
            findings.append(f"  MISSING attribute @{name}")
        elif required and m["optional"]:
            findings.append(f"  REQUIREDNESS @{name}: schema requires it, model field '{m['field']}' is Optional")
    for name in ma:
        if name not in xa:
            findings.append(f"  EXTRA attribute @{name} in model, not in schema")

    if any(p.choice_repeats for p in xe.values()):
        branches = sorted(n for n, p in xe.items() if p.choice_repeats)
        findings.append(f"  ORDERING RISK: repeating xs:choice over {branches} — model cannot round-trip interleaved children")

    return findings


def run(xsd_path, module, skip=(), locations=None):
    """locations: list of (namespace_uri, local_xsd_path) to resolve imports offline."""
    schema = xmlschema.XMLSchema(xsd_path, locations=locations)
    import importlib
    mod = importlib.import_module(module)
    print(f"\n=== {module} vs {xsd_path.split('/')[-1]} ===")
    checked = unmatched = 0
    for tname, ct in schema.types.items():
        if not isinstance(ct, xmlschema.validators.XsdComplexType) or tname in skip:
            continue
        cls = getattr(mod, tname, None)
        if cls is None or not hasattr(cls, "model_fields"):
            unmatched += 1
            print(f"[no model] {tname}")
            continue
        checked += 1
        f = compare(tname, ct, cls)
        if f:
            print(f"[{tname}]")
            print("\n".join(f))
    print(f"-- checked {checked} types, {unmatched} with no matching model")


if __name__ == "__main__":
    run("C:\\repos\\vo-models\\tests\\vodataservice\\VODataService-v1.2.xsd", "vo_models.vodataservice.models")
    # Cross-schema imports must be mapped to local files, e.g.:
    # run("tests/tapregext/TAPRegExt-v1.0-with-erratum1.xsd", "vo_models.tapregext.models",
    #     locations=[("http://www.ivoa.net/xml/VOResource/v1.0", "tests/voresource/VOResource-v1.1.xsd")])