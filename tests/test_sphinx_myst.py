from __future__ import annotations

import re
from textwrap import dedent

import pytest


@pytest.mark.integration
def test_myst_inline_and_display_math_are_native_mathml(build_sphinx) -> None:  # type: ignore[no-untyped-def]
    result, output = build_sphinx(
        {
            "conf.py": dedent(
                """
                extensions = ["myst_parser", "sphinx_typst_math"]
                html_math_renderer = "typst"
                myst_enable_extensions = ["dollarmath"]
                """
            ),
            "index.md": dedent(
                """\
                # Typst math

                Inline: $sum_(i=1)^n i$

                $$
                integral_0^1 x^2 dif x
                $$
                """
            ),
        }
    )

    assert result.returncode == 0, result.stdout + result.stderr
    html = (output / "index.html").read_text(encoding="utf-8")
    inline = re.search(r'<span class="[^"]*typst-math-inline[^"]*">(.*?)</span>', html)
    display = re.search(
        r'<div class="[^"]*typst-math-display[^"]*">(.*?)</div>', html, re.DOTALL
    )
    assert inline and "<math" in inline.group(1)
    assert inline and 'display="block"' not in inline.group(1)
    assert display and '<math display="block"' in display.group(1)
    assert "MathJax" not in html
    assert "tex-mml-chtml" not in html
    assert 'href="_static/sphinx-typst-math.css' in html
    css = (output / "_static" / "sphinx-typst-math.css").read_text(encoding="utf-8")
    assert ".typst-math mtable.multiline-equation" in css
    assert "background:" not in css


@pytest.mark.integration
def test_sphinx_equation_number_reference_and_permalink(build_sphinx) -> None:  # type: ignore[no-untyped-def]
    result, output = build_sphinx(
        {
            "conf.py": dedent(
                """
                extensions = ["sphinx_typst_math"]
                html_math_renderer = "typst"
                """
            ),
            "index.rst": dedent(
                """\
                Numbered equation
                =================

                .. math::
                   :label: energy

                   E = m c^2

                See :eq:`energy`.
                """
            ),
        }
    )

    assert result.returncode == 0, result.stdout + result.stderr
    html = (output / "index.html").read_text(encoding="utf-8")
    assert 'id="equation-energy"' in html
    assert '<span class="eqno">(1)' in html
    assert 'class="headerlink" href="#equation-energy"' in html
    assert 'href="#equation-energy">(1)</a>' in html


@pytest.mark.integration
def test_preamble_is_used_by_sphinx_build(build_sphinx) -> None:  # type: ignore[no-untyped-def]
    result, output = build_sphinx(
        {
            "conf.py": dedent(
                """
                extensions = ["sphinx_typst_math"]
                html_math_renderer = "typst"
                typst_math_preamble = "#let sq(x) = $x^2$"
                """
            ),
            "index.rst": "Inline :math:`sq(4)`.",
        }
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "<msup>" in (output / "index.html").read_text(encoding="utf-8")


@pytest.mark.integration
def test_configured_import_is_used_by_sphinx_build(build_sphinx) -> None:  # type: ignore[no-untyped-def]
    result, output = build_sphinx(
        {
            "conf.py": dedent(
                """
                extensions = ["sphinx_typst_math"]
                html_math_renderer = "typst"
                typst_math_imports = ["math.typ"]
                """
            ),
            "math.typ": "#let sq(x) = $x^2$",
            "index.rst": "Inline :math:`sq(7)`.",
        }
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "<msup>" in (output / "index.html").read_text(encoding="utf-8")
