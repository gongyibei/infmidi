# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import datetime

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'INFMIDI'
copyright = f'2022-{datetime.date.today().year}, gongyibei'
author = 'gongyibei'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    "sphinx_inline_tabs",
    'sphinx_copybutton',
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon', # Support for NumPy and Google style docstrings
]

todo_include_todos = True

# autodoc_typehints = "both"
autodoc_typehints = "description"
# autodoc_class_signature = "separated"
# autodoc_class_signature = "mixed"
# autodoc_typehints_description_target = "documented"


templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_logo = "_static/inf.webp"
html_title = "INFMIDI"


# html_theme = 'alabaster'
html_theme = 'furo'
html_static_path = ['_static']
html_css_files = [
    'css/custom.css',
]

html_theme_options = {
    "source_repository": "https://github.com/gongyibei/infmidi/",
    "source_branch": "main",
    "source_directory": "docs/",
    "sidebar_hide_name": False,
}

# pygments_style = "manni"
pygments_style = "tango"
pygments_dark_style = "stata-dark"

html_copy_source = False
html_show_sphinx = False

