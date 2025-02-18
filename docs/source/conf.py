# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from datetime import date

# Add the path to the 'src' directory
# sys.path.insert(0, os.path.abspath('../../src'))
from indradaily import __version__

project = 'indradaily'
author = 'Sneha S & Aishwarya R, ARTPARK @ IISc'

if date.today().year == 2025:
    copyright = f"{date.today().year}, {author}"
else:
    copyright = f"2025 - {date.today().year}, {author}"

version = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []
extensions = [
    'myst_parser',
    'sphinx.ext.viewcode',  # If you want to include source code
    'sphinx_design',
    'sphinx_copybutton',
    'autodoc2',
    'sphinx_togglebutton',

    # Add other extensions as needed
]

autodoc2_packages = [
    "../../src/indradaily"
]

autodoc2_output_dir = "api"  # Where API docs will be stored
autodoc2_render_plugin = "myst"  # Use Markdown output for API docs

templates_path = ['_templates']
exclude_patterns = []

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

# autodoc2_module_all_regexes: Use this if you want to respect __all__ in modules

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_title = "indradaily"
