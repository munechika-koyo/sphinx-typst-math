from __future__ import annotations

from textwrap import dedent

import pytest


@pytest.mark.integration
def test_import_entries_must_be_non_empty_strings(build_sphinx) -> None:  # type: ignore[no-untyped-def]
    result, _ = build_sphinx(
        {
            "conf.py": dedent(
                """
                extensions = ["sphinx_typst_math"]
                html_math_renderer = "typst"
                typst_math_imports = [""]
                """
            ),
            "index.rst": "Configuration error",
        }
    )

    log = result.stdout + result.stderr
    assert result.returncode != 0
    assert "typst_math_imports entries must be non-empty strings" in log


@pytest.mark.integration
def test_raise_mode_has_source_expression_and_typst_diagnostic(build_sphinx) -> None:  # type: ignore[no-untyped-def]
    result, _ = build_sphinx(
        {
            "conf.py": dedent(
                """
                extensions = ["sphinx_typst_math"]
                html_math_renderer = "typst"
                typst_math_error_mode = "raise"
                """
            ),
            "index.rst": dedent(
                """\
                Broken
                ======

                .. math::

                   sqrt(
                """
            ),
        }
    )

    log = result.stdout + result.stderr
    assert result.returncode != 0
    assert "index.rst" in log
    assert "sqrt(" in log
    assert "diagnostic" in log


@pytest.mark.integration
def test_warn_mode_renders_escaped_obvious_fallback(build_sphinx) -> None:  # type: ignore[no-untyped-def]
    result, output = build_sphinx(
        {
            "conf.py": dedent(
                """
                extensions = ["sphinx_typst_math"]
                html_math_renderer = "typst"
                typst_math_error_mode = "warn"
                """
            ),
            "index.rst": dedent(
                """\
                Broken
                ======

                .. math::

                   sqrt(<unsafe>)
                """
            ),
        },
        warning_is_error=False,
    )

    log = result.stdout + result.stderr
    assert result.returncode == 0, log
    assert "WARNING" in log
    assert "index.rst" in log
    html = (output / "index.html").read_text(encoding="utf-8")
    assert 'class="typst-math-error"' in html
    assert "&lt;unsafe&gt;" in html
    assert "<unsafe>" not in html
