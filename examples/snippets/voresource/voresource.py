from datetime import datetime, timezone

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
    Organisation,
    Relationship,
    Resource,
    ResourceName,
    Rights,
    SecurityMethod,
    Service,
    Source,
    Validation,
    WebBrowser,
    WebService,
)

# [validation-model-start]
validation = Validation(
    value=0,
    validated_by="http://uri1",
)
validation.to_xml()
# [validation-model-end]

# [validation-xml-start]
validation_xml = """
<validation validatedBy="http://uri1">0</validation>
"""  # [validation-xml-end]

# [resource-name-model-start]
resource_name = ResourceName(
    value="resource-name1",
    ivo_id="ivo://uri1",
)
resource_name.to_xml()
# [resource-name-model-end]

# [resource-name-xml-start]
resource_name_xml = """
<resourcename ivo-id="http://uri1">resource-name</resourcename>
"""  # [resource-name-xml-end]

# [date-model-start]
date = Date(
    value=datetime(1900, 1, 1),
    role="representative",
)
date.to_xml()
# [date-model-end]

# [date-xml-start]
date_xml = """
<date role="representative">1900-01-01</date>
"""  # [date-xml-end]

# [source-model-start]
source = Source(
    value="1992ApJ…400L…1W",
    format="bibcode",
)
source.to_xml()
# [source-model-end]

# [source-xml-start]
source_xml = """
<source format="bibcode">1992ApJ…400L…1W</source>
"""  # [source-xml-end]

# [rights-model-start]
rights = Rights(
    value="MIT",
    rights_uri="http://uri1",
)
rights.to_xml()
# [rights-model-end]

# [rights-xml-start]
rights_xml = """
<rights rightsURI="http://uri1">MIT</rights>
"""  # [rights-xml-end]

# [access-url-model-start]
access_url = AccessURL(
    value="http://uri1",
    use="full",
)
access_url.to_xml()
# [access-url-model-end]

# [access-url-xml-start]
access_url_xml = """
<accessURL use="full">http://uri1</accessurl>
"""  # [access-url-xml-end]

# [mirror-url-model-start]
mirror_url = MirrorURL(
    value="http://uri1",
    title="Mirror 1",
)
mirror_url.to_xml()
# [mirror-url-model-end]

# [mirror-url-xml-start]
mirror_url_xml = """
<mirrorURL title="Mirror 1">http://uri1</mirrorurl>
"""  # [mirror-url-xml-end]

# [contact-model-start]
contact = Contact(
    ivo_id="ivo://uri1",
    name="Archive Support Team",
    address="3700 San Martin Drive, Baltimore, MD 21218 USA",
    email="archive@stsci.edu",
    telephone="+1-410-338-1234",
    alt_identifier="0000-0001-2345-6789",
)
contact.to_xml()
# [contact-model-end]

# [contact-xml-start]
contact_xml = """
<contact ivo-id="ivo://uri1">
  <name>Archive Support Team</name>
  <address>3700 San Martin Drive, Baltimore, MD 21218 USA</address>
  <email>archive@stsci.edu</email>
  <telephone>+1-410-338-1234</telephone>
  <altIdentifier>0000-0001-2345-6789</altIdentifier>
</contact>
"""  # [contact-xml-end]

# [creator-model-start]
creator = Creator(
    ivo_id="ivo://uri1",
    name="Archive Support Team",
    logo="http://uri1",
    alt_identifier="http://uri2",
)
creator.to_xml()
# [creator-model-end]

# [creator-xml-start]
creator_xml = """
<creator ivo-id="http://uri1">
  <name>Archive Support Team</name>
  <logo>http://uri1</logo>
  <altIdentifier>http://uri2</altIdentifier>
</creator>
"""  # [creator-xml-end]

# [relationship-model-start]
relationship = Relationship(
    relationship_type="Cites",
    related_resource=[
        "Resource1",
        "Resource2",
    ],
)
relationship.to_xml()
# [relationship-model-end]

# [relationship-xml-start]
relationship_xml = """
<relationship>
  <relationshipType>Cites</relationshipType>
  <relatedResource>Resource1</relatedResource>
  <relatedResource>Resource2</relatedResource>
</relationship>
"""  # [relationship-xml-end]

# [security-method-model-start]
security_method = SecurityMethod(
    standard_id="http://uri1",
)
security_method.to_xml()
# [security-method-model-end]

# [security-method-xml-start]
security_method_xml = """
<securitymethod standardID="http://uri1" />
"""  # [security-method-xml-end]

# [curation-model-start]
curation = Curation(
    publisher="MAST",
    creator=creator,
    contributor="IRSA",
    date=date,
    version="1.1",
    contact=contact,
)

curation.to_xml()
# [curation-model-end]

# [curation-xml-start]
curation_xml = """
<curation>
    <publisher ivo-id="">MAST</publisher>
    <creator ivo-id="ivo://uri1">
        <name ivo-id="">Archive Support Team</name>
        <logo>http://uri1/</logo>
    </creator>
    <contributor ivo-id="">IRSA</contributor>
    <date role="representative">1900-01-01T00:00:00.000Z</date>
    <version>1.1</version>
    <contact ivo-id="ivo://uri1">
        <name ivo-id="">Archive Support Team</name>
        <address>3700 San Martin Drive, Baltimore, MD 21218 USA</address>
        <email>archive@stsci.edu</email>
        <telephone>+1-410-338-1234</telephone>
    </contact>
</curation>
"""  # [curation-xml-end]

# [content-model-start]
content = Content(
    subject="Savage Survey",
    description="Wide field survey",
    source=Source(value="1992ApJ…400L…1W", format="bibcode"),
    reference_url="http://uri1",
    type="survey",
    content_level="1",
    relationship=relationship,
)
content.to_xml()
# [content-model-end]

# [content-xml-start]
content_xml = """
<content>
    <subject>Savage Survey</subject>
    <description>Wide field survey</description>
    <source format="bibcode">1992ApJ…400L…1W</source>
    <referenceURL>http://uri1/</referenceURL>
    <type>survey</type>
    <contentLevel>1</contentLevel>
    <relationship>
        <relationshipType>Cites</relationshipType>
        <relatedResource ivo-id="">Resource1</relatedResource>
        <relatedResource ivo-id="">Resource2</relatedResource>
    </relationship>
</content>
"""  # [content-xml-end]

# [interface-model-start]
interface = Interface(
    version="1.1",
    role="std",
    type="vr:WebBrowser",
    access_url=access_url,
    mirror_url=mirror_url,
    security_method=security_method,
    test_querystring="SELECT * FROM TAP_SCHEMA.tables",
)
interface.to_xml()
# [interface-model-end]

# [interface-xml-start]
interface_xml = """
<interface version="1.1" role="std" xsi:type="vr:WebBrowser">
    <accessURL use="full">http://uri1/</accessURL>
    <mirrorURL title="Mirror 1">http://uri1/</mirrorURL>
    <securityMethod standardID="http://uri1/"/>
    <testQueryString>SELECT * FROM TAP_SCHEMA.tables</testQueryString>
</interface>
"""  # [interface-xml-end]

# [web-browser-model-start]
web_browser = WebBrowser(
    version="1.1",
    role="std",
    access_url=access_url,
    mirror_url=mirror_url,
    security_method=security_method,
    test_querystring="SELECT * FROM TAP_SCHEMA.tables",
)
web_browser.to_xml()
# [web-browser-model-end]

# [web-browser-xml-start]
web_browser_xml = """
<interface version="1.1" role="std" xsi:type="vr:WebBrowser">
    <accessURL use="full">http://uri1/</accessURL>
    <mirrorURL title="Mirror 1">http://uri1/</mirrorURL>
    <securityMethod standardID="http://uri1/"/>
    <testQueryString>SELECT * FROM TAP_SCHEMA.tables</testQueryString>
</interface>
"""  # [web-browser-xml-end]

# [resource-model-start]
resource = Resource(
    created=datetime(1900, 1, 1, tzinfo=timezone.utc),
    updated=datetime(1900, 1, 2, tzinfo=timezone.utc),
    status="active",
    version="1.1",
    validation_level=validation,
    title="Resource 1",
    short_name="Resource1",
    identifier="ivo://uri1",
    curation=curation,
    content=content,
)
resource.to_xml()
# [resource-model-end]

# [resource-xml-start]
resource_xml = """
<resource
    created="1900-01-01T00:00:00.000Z"
    updated="1900-01-02T00:00:00.000Z"
    status="active" version="1.1">
    <validationLevel validatedBy="http://uri1/">0</validationLevel>
    <title>Resource 1</title>
    <shortName>Resource1</shortName>
    <identifier>ivo://uri1</identifier>
    <curation>
        <publisher ivo-id="">MAST</publisher>
        <creator ivo-id="ivo://uri1">
            <name ivo-id="">Archive Support Team</name>
            <logo>http://uri1/</logo>
        </creator>
        <contributor ivo-id="">IRSA</contributor>
        <date role="representative">1900-01-01T00:00:00.000Z</date>
        <version>1.1</version>
        <contact ivo-id="ivo://uri1">
            <name ivo-id="">Archive Support Team</name>
            <address>3700 San Martin Drive, Baltimore, MD 21218 USA</address>
            <email>archive@stsci.edu</email>
            <telephone>+1-410-338-1234</telephone>
        </contact>
    </curation>
    <content>
        <subject>Savage Survey</subject>
        <description>Wide field survey</description>
        <source format="bibcode">1992ApJ…400L…1W</source>
        <referenceURL>http://uri1/</referenceURL>
        <type>survey</type>
        <contentLevel>1</contentLevel>
        <relationship>
            <relationshipType>Cites</relationshipType>
            <relatedResource ivo-id="">Resource1</relatedResource>
            <relatedResource ivo-id="">Resource2</relatedResource>
        </relationship>
    </content>
</resource>
"""  # [resource-xml-end]

# [organisation-model-start]
organisation = Organisation(
    created=datetime(1900, 1, 1, tzinfo=timezone.utc),
    updated=datetime(1900, 1, 2, tzinfo=timezone.utc),
    status="active",
    version="1.1",
    validation_level=validation,
    title="Resource 1",
    short_name="Resource1",
    identifier="ivo://uri1",
    curation=curation,
    content=content,
    facility="HST",
    instrument="WFPC2",
)
organisation.to_xml()
# [organisation-model-end]

# [organisation-xml-start]
organisation_xml = """
<resource
    created="1900-01-01T00:00:00.000Z"
    updated="1900-01-02T00:00:00.000Z"
    status="active" version="1.1">
    <validationLevel validatedBy="http://uri1/">0</validationLevel>
    <title>Resource 1</title>
    <shortName>Resource1</shortName>
    <identifier>ivo://uri1</identifier>
    <curation>
        <publisher ivo-id="">MAST</publisher>
        <creator ivo-id="ivo://uri1">
            <name ivo-id="">Archive Support Team</name>
            <logo>http://uri1/</logo>
        </creator>
        <contributor ivo-id="">IRSA</contributor>
        <date role="representative">1900-01-01T00:00:00.000Z</date>
        <version>1.1</version>
        <contact ivo-id="ivo://uri1">
            <name ivo-id="">Archive Support Team</name>
            <address>3700 San Martin Drive, Baltimore, MD 21218 USA</address>
            <email>archive@stsci.edu</email>
            <telephone>+1-410-338-1234</telephone>
        </contact>
    </curation>
    <content>
        <subject>Savage Survey</subject>
        <description>Wide field survey</description>
        <source format="bibcode">1992ApJ…400L…1W</source>
        <referenceURL>http://uri1/</referenceURL>
        <type>survey</type>
        <contentLevel>1</contentLevel>
        <relationship>
            <relationshipType>Cites</relationshipType>
            <relatedResource ivo-id="">Resource1</relatedResource>
            <relatedResource ivo-id="">Resource2</relatedResource>
        </relationship>
    </content>
    <facility ivo-id="">HST</facility>
    <instrument ivo-id="">WFPC2</instrument>
</resource>
"""  # [organisation-xml-end]

# [capability-model-start]
capability = Capability(
    standard_id="ivo://uri1",
    validation_level=validation,
    description="Example Capability",
    interface=interface,
)
capability.to_xml()
# [capability-model-end]

# [capability-xml-start]
capability_xml = """
<capability standardID="ivo://uri1">
    <validationLevel validatedBy="http://uri1/">0</validationLevel>
    <description>Example Capability</description>
    <interface version="1.1" role="std" xsi:type="vr:WebBrowser">
        <accessURL use="full">http://uri1/</accessURL>
        <mirrorURL title="Mirror 1">http://uri1/</mirrorURL>
        <securityMethod standardID="http://uri1/" />
        <testQueryString>SELECT * FROM TAP_SCHEMA.tables</testQueryString>
    </interface>
</capability>
"""  # [capability-xml-end]

# [service-model-start]
service = Service(
    created=datetime(1900, 1, 1, tzinfo=timezone.utc),
    updated=datetime(1900, 1, 2, tzinfo=timezone.utc),
    status="active",
    version="1.1",
    title="Example Service",
    short_name="ExampleService",
    identifier="ivo://uri1",
    curation=curation,
    content=content,
    rights=rights,
    capability=capability,
)
service.to_xml()
# [service-model-end]

# [service-xml-start]
service_xml = """
<service
    created="1900-01-01T00:00:00.000Z"
    updated="1900-01-02T00:00:00.000Z"
    status="active" version="1.1">
    <title>Example Service</title>
    <shortName>ExampleService</shortName>
    <identifier>ivo://uri1</identifier>
    <curation>
        <publisher ivo-id="">MAST</publisher>
        <creator ivo-id="ivo://uri1">
            <name ivo-id="">Archive Support Team</name>
            <logo>http://uri1/</logo>
        </creator>
        <contributor ivo-id="">IRSA</contributor>
        <date role="representative">1900-01-01T00:00:00.000Z</date>
        <version>1.1</version>
        <contact ivo-id="ivo://uri1">
            <name ivo-id="">Archive Support Team</name>
            <address>3700 San Martin Drive, Baltimore, MD 21218 USA</address>
            <email>archive@stsci.edu</email>
            <telephone>+1-410-338-1234</telephone>
        </contact>
    </curation>
    <content>
        <subject>Savage Survey</subject>
        <description>Wide field survey</description>
        <source format="bibcode">1992ApJ…400L…1W</source>
        <referenceURL>http://uri1/</referenceURL>
        <type>survey</type>
        <contentLevel>1</contentLevel>
        <relationship>
            <relationshipType>Cites</relationshipType>
            <relatedResource ivo-id="">Resource1</relatedResource>
            <relatedResource ivo-id="">Resource2</relatedResource>
        </relationship>
    </content>
    <rights rightsURI="http://uri1/">MIT</rights>
    <capability standardID="ivo://uri1">
        <validationLevel validatedBy="http://uri1/">0</validationLevel>
        <description>Example Capability</description>
        <interface version="1.1" role="std" xsi:type="vr:WebBrowser">
            <accessURL use="full">http://uri1/</accessURL>
            <mirrorURL title="Mirror 1">http://uri1/</mirrorURL>
            <securityMethod standardID="http://uri1/" />
            <testQueryString>SELECT * FROM TAP_SCHEMA.tables</testQueryString>
        </interface>
    </capability>
</service>
"""  # [service-xml-end]
