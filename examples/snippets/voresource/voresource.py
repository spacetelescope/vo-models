"""Snippets for VOResource models and XML serialization."""
from datetime import timezone as tz

from vo_models.voresource.models import (
    AccessURL,
    Capability,
    Contact,
    Content,
    Creator,
    Curation,
    Date,
    Interface,
    MirrorURL,
    Relationship,
    Resource,
    ResourceName,
    Rights,
    SecurityMethod,
    Service,
    Source,
    Validation,
)
from vo_models.voresource.types import UTCTimestamp

# pylint: disable=invalid-name

# [Resource-model-start]
resource = Resource(
    created=UTCTimestamp(1996, 3, 11, 19, 0, 0, tzinfo=tz.utc),
    updated=UTCTimestamp(1996, 3, 11, 19, 0, 0, tzinfo=tz.utc),
    status="active",
    version="1.0",
    validation_level=[Validation(value=0, validated_by="https://example.edu")],
    title="Example Resource",
    short_name="example",
    identifier="https://example.edu",
    alt_identifier=["bibcode:2008ivoa.spec.0222P"],
    curation=Curation(
        publisher=ResourceName(value="STScI"),
        creator=[Creator(name=ResourceName(value="Doe, J."))],
        contributor=[ResourceName(value="Example Resource")],
        date=[Date(value="2021-01-01T00:00:00Z", role="update")],
        version="1.0",
        contact=[Contact(name=ResourceName(value="John Doe"))],
    ),
    content=Content(
        subject=["Astronomy"],
        description="Example description",
        source=Source(value="https://example.edu", format="bibcode"),
        reference_url="https://example.edu",
        type=["Education"],
        content_level=["General"],
        relationship=[
            Relationship(
                relationship_type="isPartOf",
                related_resource=[ResourceName(value="Example Resource", ivo_id="ivo://example.edu/resource")],
            )
        ],
    ),
)
# [Resource-model-end]

# [Resource-xml-start]
resource_xml = """
<vr:Resource xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" created="1996-03-11T19:00:00.000Z"
        updated="1996-03-11T19:00:00.000Z" status="active" version="1.0">
        <vr:validationLevel validatedBy="https://example.edu/">0</vr:validationLevel>
        <vr:title>Example Resource</vr:title>
        <vr:shortName>example</vr:shortName>
        <vr:identifier>https://example.edu/</vr:identifier>
        <vr:altIdentifier>bibcode:2008ivoa.spec.0222P</vr:altIdentifier>
        <vr:curation>
                <vr:publisher>STScI</vr:publisher>
                <vr:creator>
                        <vr:name>Doe, J.</vr:name>
                </vr:creator>
                <vr:contributor>Example Resource</vr:contributor>
                <vr:date role="update">2021-01-01T00:00:00.000Z</vr:date>
                <vr:version>1.0</vr:version>
                <vr:contact>
                        <vr:name>John Doe</vr:name>
                </vr:contact>
        </vr:curation>
        <vr:content>
                <vr:subject>Astronomy</vr:subject>
                <vr:description>Example description</vr:description>
                <vr:source format="bibcode">https://example.edu/</vr:source>
                <vr:referenceURL>https://example.edu/</vr:referenceURL>
                <vr:type>Education</vr:type>
                <vr:contentLevel>General</vr:contentLevel>
                <vr:relationship>
                        <vr:relationshipType>isPartOf</vr:relationshipType>
                        <vr:relatedResource ivo-id="ivo://example.edu/resource">Example Resource</vr:relatedResource>
                </vr:relationship>
        </vr:content>
</vr:Resource>
"""  # [Resource-xml-end]

# [Service-model-start]
service = Service(
    created=UTCTimestamp(1996, 3, 11, 19, 0, 0, tzinfo=tz.utc),
    updated=UTCTimestamp(1996, 3, 11, 19, 0, 0, tzinfo=tz.utc),
    status="active",
    title="Example Service",
    identifier="https://example.edu",
    curation=Curation(
        publisher=ResourceName(value="STScI"),
        creator=[Creator(name=ResourceName(value="Doe, J."))],
        contributor=[ResourceName(value="Example Resource")],
        date=[Date(value="2021-01-01T00:00:00Z", role="update")],
        version="1.0",
        contact=[Contact(name=ResourceName(value="John Doe"))],
    ),
    content=Content(
        subject=["Astronomy"],
        description="Example description",
        source=Source(value="https://example.edu", format="bibcode"),
        reference_url="https://example.edu",
        type=["Education"],
        content_level=["General"],
        relationship=[
            Relationship(
                relationship_type="isPartOf",
                related_resource=[ResourceName(value="Example Resource", ivo_id="ivo://example.edu/resource")],
            )
        ],
    ),
    rights=[Rights(value="CC BY 4.0", rights_uri="https://creativecommons.org/licenses/by/4.0/")],
    capability=[Capability(standard_id="ivo://ivoa.net/std/TAP")],
)
# [Service-model-end]

# [Service-xml-start]
service_xml = """
<vr:Service xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" created="1996-03-11T19:00:00.000Z"
        updated="1996-03-11T19:00:00.000Z" status="active">
        <vr:title>Example Service</vr:title>
        <vr:identifier>https://example.edu/</vr:identifier>
        <vr:curation>
                <vr:publisher>STScI</vr:publisher>
                <vr:creator>
                        <vr:name>Doe, J.</vr:name>
                </vr:creator>
                <vr:contributor>Example Resource</vr:contributor>
                <vr:date role="update">2021-01-01T00:00:00.000Z</vr:date>
                <vr:version>1.0</vr:version>
                <vr:contact>
                        <vr:name>John Doe</vr:name>
                </vr:contact>
        </vr:curation>
        <vr:content>
                <vr:subject>Astronomy</vr:subject>
                <vr:description>Example description</vr:description>
                <vr:source format="bibcode">https://example.edu/</vr:source>
                <vr:referenceURL>https://example.edu/</vr:referenceURL>
                <vr:type>Education</vr:type>
                <vr:contentLevel>General</vr:contentLevel>
                <vr:relationship>
                        <vr:relationshipType>isPartOf</vr:relationshipType>
                        <vr:relatedResource ivo-id="ivo://example.edu/resource">Example Resource</vr:relatedResource>
                </vr:relationship>
        </vr:content>
        <vr:rights rightsURI='https://creativecommons.org/licenses/by/4.0/'>CC BY 4.0</vr:rights>
        <vr:capability standardID='ivo://ivoa.net/std/TAP' />
</vr:Service>
"""  # [Service-xml-end]

# [Capability-model-start]
capability_model = Capability(
    standard_id="ivo://ivoa.net/std/TAP",
    validation_level=[Validation(value=0, validated_by="https://example.edu")],
    description="Example description",
    interface=[Interface(version="1.0", role="std", access_url=[AccessURL(value="https://example.edu", use="full")])],
)
# [Capability-model-end]

# [Capability-xml-start]
capability_xml = """
<vr:Capability xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0"
        standardID="ivo://ivoa.net/std/TAP">
        <vr:validationLevel validatedBy="https://example.edu/">0</vr:validationLevel>
        <vr:description>Example description</vr:description>
        <vr:interface role="std" version="1.0">
                <vr:accessURL use="full">https://example.edu/</vr:accessURL>
        </vr:interface>
</vr:Capability>
"""  # [Capability-xml-end]

# [Interface-model-start]
interface_model = Interface(
    version="1.0",
    role="std",
    access_url=[AccessURL(value="https://example.edu", use="full")],
    mirror_url=[MirrorURL(value="https://example.edu", title="Mirror")],
    security_method=[SecurityMethod(standard_id="ivo://ivoa.net/std/Security#basic")],
    test_querystring="test",
)
# [Interface-model-end]

# [Interface-xml-start]
interface_xml = """
<vr:Interface xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0" role="std" version="1.0">
        <vr:accessURL use="full">https://example.edu/</vr:accessURL>
        <vr:mirrorURL title="Mirror">https://example.edu/</vr:mirrorURL>
        <vr:securityMethod standardID="ivo://ivoa.net/std/Security#basic" />
        <vr:testQueryString>test</vr:testQueryString>
</vr:Interface>
"""  # [Interface-xml-end]
