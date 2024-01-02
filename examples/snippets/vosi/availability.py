from vo_models.vosi.availability import Availability

# [model-start]
availability = Availability(
    available=True,
    up_since="2023-01-01T00:00:00Z",
    down_at="2023-01-02T00:00:00Z",
    back_at="2023-01-03T00:00:00Z",
    notes=["This service is available for public use."],
)

availability.to_xml()
# [model-end]

# [xml-start]
avail_xml = """
<availability
    xmlns="http://www.ivoa.net/xml/VOSIAvailability/v1.0"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<available>true</available>
<upSince>2023-01-01T00:00:00.000Z</upSince>
<downAt>2023-01-02T00:00:00.000Z</downAt>
<backAt>2023-01-03T00:00:00.000Z</backAt>
</availability>
"""
# [xml-end]