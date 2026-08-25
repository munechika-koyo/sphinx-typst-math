from __future__ import annotations

import pytest

from sphinx_typst_math.backend import MathRenderingError
from sphinx_typst_math.mathml import extract_mathml


def test_extracts_one_math_element_without_surrounding_html() -> None:
    html = (
        "<!doctype html><html><body><p>before "
        '<math display="inline"><mi>x</mi><mo>&amp;</mo></math>'
        " after</p></body></html>"
    )

    assert extract_mathml(html) == (
        '<math display="inline"><mi>x</mi><mo>&amp;</mo></math>'
    )


@pytest.mark.parametrize(
    "html, count",
    [
        ("<html><body>none</body></html>", 0),
        ("<math><mi>x</mi></math><math><mi>y</mi></math>", 2),
    ],
)
def test_requires_exactly_one_math_element(html: str, count: int) -> None:
    with pytest.raises(MathRenderingError, match=f"found {count}"):
        extract_mathml(html)


def test_rejects_unclosed_math_element() -> None:
    with pytest.raises(MathRenderingError, match="unclosed"):
        extract_mathml("<html><math><mi>x</mi></html>")


def test_accepts_utf8_bytes() -> None:
    assert extract_mathml("<math><mi>π</mi></math>".encode()) == (
        "<math><mi>π</mi></math>"
    )
