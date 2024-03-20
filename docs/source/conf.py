# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
from pathlib import Path

import toml

ROOT_PATH = Path(__file__).parent.parent.parent
CONF_PATH = ROOT_PATH / "pyproject.toml"
sys.path.insert(0, str(ROOT_PATH.absolute()))

PYPROJECT = toml.load(CONF_PATH)["project"]

project = PYPROJECT["name"]
release = PYPROJECT["version"]
author = f"{PYPROJECT['authors'][0]['name']} <{PYPROJECT['authors'][0]['email']}>"
copyright = "2023, Joshua Fraustro"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]

autodoc_default_options = {
    "no-inherited-members": None,
    "exclude-members": "model_config, model_fields",
}

autodoc_typehints = "description"
autodoc_typehints_format = "short"
autodoc_member_order = "bysource"

autoclass_content = "class"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "lxml": ("https://lxml.de/apidoc/", None),
}

autosectionlabel_prefix_document = True

html_theme_options = {}
html_title = PYPROJECT["name"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
