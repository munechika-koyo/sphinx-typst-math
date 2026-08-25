from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from sphinx_typst_math.backend import MathRenderingError
from sphinx_typst_math.backends.typst import TypstBackend, _make_document


def test_official_compiler_emits_inline_mathml() -> None:
    mathml = TypstBackend().render("sum_(i=1)^n i", display=False)

    assert mathml.startswith("<math")
    assert 'display="block"' not in mathml
    assert "<msubsup>" in mathml


def test_official_compiler_emits_block_mathml() -> None:
    mathml = TypstBackend().render("integral_0^1 x^2 dif x", display=True)

    assert mathml.startswith("<math")
    assert 'display="block"' in mathml
    assert "<msubsup>" in mathml


def test_preamble_definitions_are_available() -> None:
    backend = TypstBackend(preamble="#let sq(x) = $x^2$")

    assert "<msup>" in backend.render("sq(3)", display=False)


def test_preamble_imports_resolve_from_sphinx_source_root(tmp_path: Path) -> None:
    (tmp_path / "math.typ").write_text("#let sq(x) = $x^2$", encoding="utf-8")
    backend = TypstBackend(preamble='#import "math.typ": sq', root=tmp_path)

    assert "<msup>" in backend.render("sq(5)", display=False)


def test_configured_imports_import_all_from_sphinx_source_root(tmp_path: Path) -> None:
    (tmp_path / "math.typ").write_text("#let sq(x) = $x^2$", encoding="utf-8")
    backend = TypstBackend(imports=["math.typ"], root=tmp_path)

    assert "<msup>" in backend.render("sq(6)", display=False)


def test_cache_avoids_duplicate_compilation() -> None:
    backend = TypstBackend(cache=True)
    real_compiler = backend._compiler

    class CountingCompiler:
        calls = 0

        def compile(self, **kwargs: Any) -> bytes:
            self.calls += 1
            result = real_compiler.compile(**kwargs)
            assert isinstance(result, bytes)
            return result

    compiler = CountingCompiler()
    backend._compiler = compiler  # type: ignore[assignment]

    first = backend.render("x^2", display=False)
    second = backend.render("x^2", display=False)

    assert first == second
    assert compiler.calls == 1
    assert backend.cache_size == 1


def test_display_mode_and_preamble_are_part_of_cache_identity() -> None:
    backend = TypstBackend(cache=True)
    backend.render("x", display=False)
    backend.render("x", display=True)
    backend.preamble = "#let y = 1"
    backend.render("x", display=True)

    assert backend.cache_size == 3


def test_imports_are_part_of_cache_identity() -> None:
    backend = TypstBackend(cache=True)

    class CountingCompiler:
        calls = 0

        def compile(self, **kwargs: Any) -> bytes:
            del kwargs
            self.calls += 1
            return b"<html><body><math><mi>x</mi></math></body></html>"

    compiler = CountingCompiler()
    backend._compiler = compiler  # type: ignore[assignment]
    backend.render("x", display=False)
    backend.imports = ("different.typ",)
    backend.render("x", display=False)

    assert compiler.calls == 2
    assert backend.cache_size == 2


def test_invalid_typst_reports_expression_and_diagnostic() -> None:
    with pytest.raises(MathRenderingError) as exc_info:
        TypstBackend().render("sqrt(", display=False)

    message = str(exc_info.value)
    assert "sqrt(" in message
    assert "diagnostic" in message


def test_document_wrapper_uses_typst_spacing_for_display_mode() -> None:
    assert _make_document("x", display=False, preamble="") == "$x$\n"
    assert _make_document("x", display=True, preamble="") == "$ x $\n"


def test_document_wrapper_places_imports_before_preamble() -> None:
    document = _make_document(
        "sq(2)",
        display=False,
        preamble="#let local = 1",
        imports=["@preview/physica:0.9.8", 'quote"test.typ'],
    )

    assert document == (
        '#import "@preview/physica:0.9.8": *\n'
        '#import "quote\\"test.typ": *\n'
        "#let local = 1\n"
        "$sq(2)$\n"
    )
