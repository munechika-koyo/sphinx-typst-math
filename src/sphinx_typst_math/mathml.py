"""Extraction of MathML from a standalone Typst HTML document."""

from __future__ import annotations

from html.parser import HTMLParser

from .backend import MathRenderingError


class _MathExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.elements: list[str] = []
        self._parts: list[str] | None = None
        self._depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag == "math":
            if self._parts is not None:
                self._depth += 1
            else:
                self._parts = []
                self._depth = 1
        if self._parts is not None:
            self._parts.append(self._starttag_text())

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag == "math" and self._parts is None:
            self.elements.append(self._starttag_text())
        elif self._parts is not None:
            self._parts.append(self._starttag_text())

    def _starttag_text(self) -> str:
        text = self.get_starttag_text()
        if text is None:
            raise MathRenderingError("HTML parser did not retain a start tag")
        return text

    def handle_endtag(self, tag: str) -> None:
        if self._parts is None:
            return
        self._parts.append(f"</{tag}>")
        if tag == "math":
            self._depth -= 1
            if self._depth == 0:
                self.elements.append("".join(self._parts))
                self._parts = None

    def handle_data(self, data: str) -> None:
        if self._parts is not None:
            self._parts.append(data)

    def handle_entityref(self, name: str) -> None:
        if self._parts is not None:
            self._parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self._parts is not None:
            self._parts.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        if self._parts is not None:
            self._parts.append(f"<!--{data}-->")


def extract_mathml(html: str | bytes) -> str:
    """Extract exactly one complete ``math`` element from an HTML document."""
    if isinstance(html, bytes):
        try:
            html = html.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise MathRenderingError("Typst returned non-UTF-8 HTML") from exc

    parser = _MathExtractor()
    parser.feed(html)
    parser.close()

    if parser._parts is not None:
        raise MathRenderingError("Typst HTML contains an unclosed MathML element")
    if len(parser.elements) != 1:
        raise MathRenderingError(
            "expected exactly one MathML element in Typst HTML, "
            f"found {len(parser.elements)}"
        )
    return parser.elements[0]
