import os
import sys

sys.path.insert(0, os.path.abspath("."))

project = "DRIAMS Federated AMR Analysis"
copyright = "2025"
author = ""
release = "1.0"

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Docs/_build", "Docs/_static"]
source_suffix = ".rst"
master_doc = "index"

html_theme = "sphinx_rtd_theme"
html_static_path = ["Docs/_static"]
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
    "sticky_navigation": True,
}

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
