# sphinx-typst-math

`sphinx-typst-math` is a Sphinx HTML math renderer for **native Typst math
syntax**. It sends each equation to the official Typst compiler through
[`typst-py`](https://github.com/messense/typst-py), extracts the compiler's
MathML, and places that MathML directly into Sphinx's HTML.

There is no Typst-to-LaTeX conversion, MathJax runtime, custom math parser, or
Node.js dependency.

> [!IMPORTANT]
> Typst 0.15 introduced HTML equation export. This package therefore requires
> `typst-py >= 0.15`.

## Installation

```bash
pip install sphinx-typst-math
```

MyST Parser, nbsphinx, and sphinx-immaterial are optional integrations. Install
the ones used by your documentation project separately.

## Quick start

```python
# conf.py

extensions = [
    "myst_parser",
    "nbsphinx",
    "sphinx_typst_math",
]

html_math_renderer = "typst"

myst_enable_extensions = [
    "dollarmath",
]
```

Then use Typst—not LaTeX—between Markdown math delimiters:

```markdown
$sum_(i=1)^n x_i$

$$
integral_0^infinity e^(-x^2) dif x
= sqrt(pi) / 2
$$
```

The same Markdown can be placed in a Jupyter notebook Markdown cell when the
notebook is built by nbsphinx and Sphinx. JupyterLab's own live Markdown
preview is separate from a Sphinx build and may still use MathJax, so it may
not preview Typst syntax correctly.

Do not enable `sphinx.ext.mathjax`; it is not needed. If another extension has
registered a math renderer, keep `html_math_renderer = "typst"` explicit.

## Configuration

```python
html_math_renderer = "typst"

# Each entry is imported with `: *` before the preamble and equation.
typst_math_imports = [
    "@preview/physica:0.9.8",
]

# Inserted after imports and immediately before each equation. Useful for
# shared definitions and selective import statements.
typst_math_preamble = """
#let sq(x) = $x^2$
"""

# "raise" stops the build; "warn" emits a warning and escaped fallback markup.
typst_math_error_mode = "raise"

# Cache equal source/display/import/preamble/compiler combinations for this build.
typst_math_cache = True
```

Every `typst_math_imports` entry expands to `#import "…": *`. Typst packages
must include their namespace and exact version. Local import paths and relative
preamble imports resolve from the Sphinx source directory. For a selective
import, put the complete statement in `typst_math_preamble` instead:

```python
typst_math_preamble = r"""
#import "@preview/physica:0.9.8": dv, pdv
"""
```

Imports, the preamble, and equation source are evaluated by the real Typst compiler.
Sphinx source files and configuration are therefore assumed to be trusted
build inputs.

## Equation numbers and references

The renderer retains the IDs and numbering assigned structurally by Sphinx.
For example, a labeled reStructuredText equation works with Sphinx's normal
equation role:

```rst
.. math::
   :label: energy

   E = m c^2

See :eq:`energy`.
```

Typst source is not inspected for LaTeX commands such as `\label`, `\tag`, or
`\eqref`. Labels must be represented by Sphinx/MyST nodes. In particular,
notebook labels that depend on LaTeX-internal commands are not supported in
the first release.

## HTML and theme behavior

Inline nodes use a standard Sphinx `span.math` wrapper. Display nodes use a
standard `div.math` wrapper, including Sphinx's `eqno` and `headerlink` markup
when numbered. The equation itself is native MathML, inherits the surrounding
text color, and has no hard-coded background. This also keeps the renderer
compatible with sphinx-immaterial light and dark color schemes without
theme-specific CSS.

This extension changes HTML math rendering only. Other Sphinx builders retain
their own math handling and may still expect LaTeX input.

## Alternative backends

The first release intentionally has no Kern backend. Kern is a useful
JavaScript renderer with its own Typst-like lexer, parser, and MathML emitter,
but it is not the official Typst compiler and documents parity gaps for some
constructs. Adding it would also introduce a separate compatibility surface
and potentially a Node.js workflow. It can be reconsidered later as an
explicit opt-in backend; it is not suitable as the compatibility-preserving
default.

## Development

The repository includes a Pixi environment with Python dependencies and
Pandoc (needed by nbsphinx tests):

```bash
pixi install
pixi run check
```

The test suite compiles real Typst equations and builds real MyST, nbsphinx,
and sphinx-immaterial projects.
