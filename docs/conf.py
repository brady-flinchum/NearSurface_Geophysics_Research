# Configuration file for the Sphinx documentation builder.
import os, sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -------------------------------------------------------
project   = 'Your Name – Research'
copyright = '2024, Your Name'
author    = 'Your Name'
release   = '1.0'

# -- Extensions ----------------------------------------------------------------
extensions = [
    'sphinx.ext.mathjax',       # LaTeX math in pages
    'sphinx.ext.autodoc',       # auto-document Python modules
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'myst_parser',              # .md pages
    'nbsphinx',                 # Jupyter notebooks
    'sphinxcontrib.bibtex',     # citations from .bib
    'sphinx_copybutton',
    'sphinx_design',
    'jupyter_sphinx',
]

# -- File types ----------------------------------------------------------------
source_suffix = {
    '.rst': 'restructuredtext',
    '.md':  'markdown',
}

# -- MyST settings (Markdown extensions) --------------------------------------
myst_enable_extensions = [
    'dollarmath',       # $...$ and $$...$$ for inline/block math
    'colon_fence',      # ::: directives
    'deflist',
    'tasklist',
]
myst_dmath_double_inline = True

# -- nbsphinx (Jupyter notebook) settings -------------------------------------
nbsphinx_execute = 'always'          # re-run notebooks on every build
nbsphinx_timeout = 120               # seconds; increase for heavy PyVista renders
nbsphinx_kernel_name = 'python3'

# PyVista: use static screenshots in CI (no display available)
import pyvista as pv
pv.OFF_SCREEN = True
pv.set_jupyter_backend('static')     # swap to 'trame' locally for interactivity

# -- BibTeX --------------------------------------------------------------------
bibtex_bibfiles = ['refs.bib']
bibtex_default_style = 'unsrt'

# -- HTML output ---------------------------------------------------------------
html_theme = 'pydata_sphinx_theme'

html_theme_options = {
    'github_url':        'https://github.com/YOUR_USERNAME/YOUR_REPO',
    'navbar_center':     ['navbar-nav'],
    'navbar_end':        ['navbar-icon-links'],
    'footer_start':      ['copyright'],
    'secondary_sidebar_items': ['page-toc', 'sourcelink'],
    'show_toc_level':    2,
    'logo': {
        'text': 'Your Name',
    },
    'navigation_with_keys': True,
}

html_sidebars = {
    '**': ['sidebar-nav-bs'],
}

html_title       = 'Your Name – Research'
html_static_path = ['_static']
html_css_files   = ['custom.css']

# -- Math ----------------------------------------------------------------------
mathjax3_config = {
    'tex': {
        'packages': {'[+]': ['ams', 'physics']},
    }
}

# -- Exclude patterns ----------------------------------------------------------
exclude_patterns = ['_build', '**.ipynb_checkpoints', 'Thumbs.db', '.DS_Store']
