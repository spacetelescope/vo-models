from enum import Enum
from typing import Union, get_args, get_origin

from pydantic_core import PydanticUndefined, Url
from pydantic_xml import BaseXmlModel

from vo_models.voresource.models import Capability


def get_default_for_type(annotation):
    """Return a default value for a primitive type."""
    if annotation == str:
        return ""
    elif annotation == int:
        return 0
    elif annotation == float:
        return 0.0
    elif annotation == bool:
        return False
    elif annotation == list:
        return []
    elif annotation == dict:
        return {}
    elif annotation == Url:
        return Url("http://example.com")
    elif issubclass(annotation, Enum):
        return list(annotation)[0]
    return None  # For other unhandled types


def create_example_instance(model_cls: BaseXmlModel):
    # Get the schema, which contains the examples
    schema = model_cls.model_json_schema()

    # Prepare a dictionary to hold the example values
    example_values = {}

    for field, prop in schema.get("properties", {}).items():
        field_info = model_cls.model_fields[field]
        field_annotation = field_info.annotation  # Use annotation in pydantic-xml

        # If the field has an example, use it
        if "examples" in prop:
            example_values[field] = prop["examples"]
        elif field_info.default not in (None, PydanticUndefined):
            example_values[field] = field_info.default
        elif "enum" in prop:
            example_values[field] = prop["enum"][0]
        else:
            origin = get_origin(field_annotation)
            if origin == list:
                # Recursive case: field is a list of submodels
                submodel = get_args(field_annotation)[0]  # Get the type inside the list
                if issubclass(submodel, BaseXmlModel):
                    example_values[field] = [create_example_instance(submodel)]
                else:
                    example_values[field] = []
            elif origin == Union:
                # Recursive case: field is a union of submodels or Optional (Union with None)
                submodels = get_args(field_annotation)
                for submodel in submodels:
                    if get_origin(submodel) == list:
                        submodel = get_args(submodel)[0]
                        if issubclass(submodel, BaseXmlModel):
                            example_values[field] = [create_example_instance(submodel)]
                            break
                    elif issubclass(submodel, BaseXmlModel):
                        example_values[field] = create_example_instance(submodel)
                        break
                    else:
                        example_values[field] = get_default_for_type(submodel)
            elif issubclass(field_annotation, BaseXmlModel):
                # Recursive case: field is a submodel
                example_values[field] = create_example_instance(field_annotation)
            else:
                # For primitive types with no example, use default values
                example_values[field] = get_default_for_type(field_annotation)

    # Create an instance of the model with the example values
    instance = model_cls(**example_values)

    # Return the instance's __repr__ output
    return instance


print(create_example_instance(Capability).to_xml(encoding=str, pretty_print=True))
