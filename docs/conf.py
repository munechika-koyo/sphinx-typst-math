"""Sphinx configuration for the sphinx-typst-math demonstration."""

from datetime import date

from packaging.version import parse

from sphinx_typst_math import __version__

# -- Project information -----------------------------------------------------
project = "sphinx-typst-math"
author = "Koyo Munechika"
copyright = f"2026-{date.today().year}, {author}"
version_obj = parse(__version__)
release = version_obj.public

gh_user_repo = "munechika-koyo/sphinx-typst-math"
repository_url = f"https://github.com/{gh_user_repo}"
repository_main_branch = "main"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx_immaterial",
    "sphinx_immaterial.theme_result",
    "myst_parser",
    "nbsphinx",
    "sphinx_typst_math",
]

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**.ipynb_checkpoints",
]

default_role = "obj"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

# -- MyST configuration ------------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "dollarmath",
]
myst_heading_anchors = 3

# -- sphinx-typst-math configuration ----------------------------------------
# Keep this explicit if another extension also registers an HTML math renderer.
html_math_renderer = "typst"

# Each entry becomes `#import "...": *` before every expression. Typst Universe
# packages are downloaded by Typst on the first documentation build and cached.
typst_math_imports = [
    "@preview/physica:0.9.8",
]

# Selective imports and project-wide definitions belong in the preamble.
typst_math_preamble = r"""
#import "@preview/mitex:0.2.7": mi
#import "@preview/quick-maths:0.2.1": shorthands

#show: shorthands.with(
  ($+-$, $plus.minus$),
  ($|-$, math.tack),
)

#let expectation(x) = $upright(E) lr([#x])$
"""

typst_math_error_mode = "raise"
typst_math_cache = True

# -- nbsphinx configuration --------------------------------------------------
# The demonstration notebook contains authored Markdown and an unexecuted code
# cell, so documentation builds stay deterministic and do not need a kernel.
nbsphinx_execute = "never"
nbsphinx_allow_errors = False

# -- HTML output -------------------------------------------------------------
html_theme = "sphinx_immaterial"
html_title = project
html_theme_options = {
    "repo_url": repository_url,
    "repo_name": "GitHub",
    "edit_uri": f"blob/{repository_main_branch}/docs/",
    "icon": {"repo": "fontawesome/brands/github"},
    "features": [
        "navigation.expand",
        "navigation.sections",
        "navigation.top",
        "navigation.footer",
        "search.highlight",
        "search.share",
        "search.suggest",
        "toc.follow",
        "toc.sticky",
        "content.tooltips",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "indigo",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "indigo",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to light mode",
            },
        },
    ],
}
