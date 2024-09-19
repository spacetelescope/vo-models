"""Tests for VOResource models."""

from unittest import TestCase
from xml.etree.ElementTree import canonicalize

from lxml import etree

from vo_models.voresource import (
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
