from typing import Optional

from pydantic_xml import BaseXmlModel, attr

country_wo_name = """<Country code="GER"></Country>"""
country_w_name = """<Country code="GER">Germany</Country>"""


class Country(BaseXmlModel):
    name: Optional[str] = None
    code: str = attr()


named_country = Country.from_xml(country_w_name)
unnamed_country = Country.from_xml(country_wo_name)

print(named_country.to_xml())
# <Country code="GER">Germany</Country>
print(unnamed_country.to_xml())
# <Country code="GER"></Country>
