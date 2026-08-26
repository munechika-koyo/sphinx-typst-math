from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest


@pytest.mark.integration
def test_sphinx_immaterial_builds_without_mathjax_assets(
    build_sphinx, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:  # type: ignore[no-untyped-def]
    # sphinx-immaterial evaluates its default user cache directory during Sphinx's
    # config type check.  The isolated Windows package-test user has no usable
    # Local AppData directory, so make the cache location explicit.
    monkeypatch.setenv(
        "SPHINX_IMMATERIAL_EXTERNAL_RESOURCE_CACHE_DIR",
        str(tmp_path / "sphinx-immaterial-cache"),
    )
    result, output = build_sphinx(
        {
            "conf.py": dedent(
                """
                extensions = ["sphinx_immaterial", "myst_parser", "sphinx_typst_math"]
                html_theme = "sphinx_immaterial"
                html_theme_options = {"font": False}
                html_math_renderer = "typst"
                myst_enable_extensions = ["dollarmath"]
                """
            ),
            "index.md": dedent(
                """\
                # Immaterial

                Inline $x^2$ text.

                $$
                sum_(i=1)^n i
                $$
                """
            ),
        }
    )

    assert result.returncode == 0, result.stdout + result.stderr
    html = (output / "index.html").read_text(encoding="utf-8")
    assert html.count("<math") == 2
    assert "typst-math-inline" in html
    assert "typst-math-display" in html
    assert "MathJax" not in html
    assert "background: white" not in html
