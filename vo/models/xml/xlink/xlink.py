"""Simple types for xlink schema"""
from enum import Enum


class XlinkType(str, Enum):
    """xlink 'type' values"""

    SIMPLE = "simple"
    EXTENDED = "extended"
    LOCATOR = "locator"
    ARC = "arc"
    RESOURCE = "resource"
    TITLE = "title"
