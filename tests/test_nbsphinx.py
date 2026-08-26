from __future__ import annotations

import json
from textwrap import dedent

import nbsphinx
import pytest

NOTEBOOK_MARKDOWN = dedent(
    """\
    # Notebook

    Inline: $sum_(i=1)^n i$

    $$
    integral_0^1 x^2 dif x
    $$
    """
)


def test_nbsphinx_pandoc_conversion_preserves_literal_typst_source() -> None:
    rst = nbsphinx.markdown2rst(NOTEBOOK_MARKDOWN)

    assert "sum_(i=1)^n i" in rst
    assert "integral_0^1 x^2 dif x" in rst


@pytest.mark.integration
def test_notebook_markdown_math_is_native_mathml(build_sphinx) -> None:  # type: ignore[no-untyped-def]
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": NOTEBOOK_MARKDOWN.splitlines(keepends=True),
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    result, output = build_sphinx(
        {
            "conf.py": dedent(
                """
                extensions = ["nbsphinx", "sphinx_typst_math"]
                html_math_renderer = "typst"
                nbsphinx_execute = "never"
                exclude_patterns = ["**.ipynb_checkpoints"]
                """
            ),
            "index.rst": dedent(
                """\
                Notebook test
                =============

                .. toctree::

                   notebook
                """
            ),
            "notebook.ipynb": json.dumps(notebook),
        }
    )

    assert result.returncode == 0, result.stdout + result.stderr
    html = (output / "notebook.html").read_text(encoding="utf-8")
    assert html.count("<math") == 2
    assert "typst-math-inline" in html
    assert "typst-math-display" in html
    assert '<math display="block"' in html
    assert "MathJax" not in html
    assert "tex-mml-chtml" not in html
