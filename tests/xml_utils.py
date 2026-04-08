"""Utilities for XML schema loading in tests.

Provides a custom lxml resolver that fetches remote schemas using requests,
since newer versions of libxml2 (>= 2.14) no longer support HTTP/FTP fetching natively.
"""

import requests
from lxml import etree

requests_session = requests.Session()


class URLResolver(etree.Resolver):
    """An lxml resolver that fetches remote schemas via requests."""

    def resolve(self, schema_url, public_id, context):  # pylint: disable=unused-argument
        if schema_url and schema_url.startswith(("http://", "https://")):
            response = requests_session.get(schema_url, timeout=30)
            response.raise_for_status()
            return self.resolve_string(response.content, context)
        return None


def load_schema(path: str) -> etree.XMLSchema:
    """Parse an XSD file into an XMLSchema, resolving remote imports via requests."""
    parser = etree.XMLParser()
    parser.resolvers.add(URLResolver())
    with open(path, "r") as f:
        schema_doc = etree.parse(f, parser)
    return etree.XMLSchema(schema_doc)
