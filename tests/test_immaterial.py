from __future__ import annotations

import pytest


@pytest.mark.integration
def test_sphinx_immaterial_builds_without_mathjax_assets(build_sphinx) -> None:  # type: ignore[no-untyped-def]
    result, output = build_sphinx(
        {
            "conf.py": """
extensions = ["sphinx_immaterial", "myst_parser", "sphinx_typst_math"]
html_theme = "sphinx_immaterial"
html_theme_options = {"font": False}
html_math_renderer = "typst"
myst_enable_extensions = ["dollarmath"]
""",
            "index.md": """# Immaterial

Inline $x^2$ text.

$$
sum_(i=1)^n i
$$
""",
        }
    )

    assert result.returncode == 0, result.stdout + result.stderr
    html = (output / "index.html").read_text(encoding="utf-8")
    assert html.count("<math") == 2
    assert "typst-math-inline" in html
    assert "typst-math-display" in html
    assert "MathJax" not in html
    assert "background: white" not in html
