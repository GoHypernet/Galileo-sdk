# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

from os import path
import sys
import sphinx_material

root = path.realpath(path.join(path.dirname(__file__), '..', '..'))
sys.path.insert(1, root)
import galileo_sdk

autodoc_default_flags = ['members']
autosummary_generate = True
autosummary_imported_members = True

# -- Python specific configuration -------------------------------------------


# Make sure that __init__ methods are documented
def skip(app, what, name, obj, would_skip, options):
    if name == "__init__":
        return False
    return would_skip


def setup(app):
    app.connect("autodoc-skip-member", skip)


# -- Project information -----------------------------------------------------

project = "Galileo"
copyright = "2020, Hypernet Labs"
author = "Hypernet Labs"

# The full version, including alpha/beta/rc tags
# release = "0.0.13"

# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx_material",
    "sphinx.ext.autosummary",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# Choose the material theme
html_theme = "sphinx_material"
# Get the them path
html_theme_path = sphinx_material.html_theme_path()
# Register the required helpers for the html context
html_context = sphinx_material.get_html_context()

html_theme_options = {
    "repo_name": "Galileo-sdk",
    "repo_url": "https://github.com/GoHypernet/Galileo-sdk",
    "html_minify": True,
    "css_minify": True,
    "nav_title": "Galileo Documentation",
    "globaltoc_depth": 3,
    "theme_color": "#4dc1ab",
    "color_primary": "teal",
    "globaltoc_collapse": True,
    "globaltoc_includehidden": True,
    "version_dropdown": False,
}

html_sidebars = {"**": ["globaltoc.html"]}

html_logo = "_static/galileo-logo.png"
html_favicon = "_static/galileo-icon.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

keep_warnings = False
