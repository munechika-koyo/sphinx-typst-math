# sphinx-typst-math

`sphinx-typst-math` renders native Typst equations as MathML in Sphinx HTML
documentation. The equations below are compiled by the official Typst compiler;
MathJax, a Typst-to-LaTeX conversion, and a browser-side JavaScript renderer are
not involved.

```{toctree}
:maxdepth: 2
:hidden:

package-examples
notebook
```

## Installation

Install the extension together with the integrations used by this demonstration:

```console
pip install sphinx-typst-math myst-parser nbsphinx sphinx-immaterial
```

Enable the extensions and select the Typst renderer in `conf.py`:

```python
extensions = [
    "sphinx_immaterial",
    "sphinx_immaterial.theme_result",
    "myst_parser",
    "nbsphinx",
    "sphinx_typst_math",
]

html_math_renderer = "typst"
myst_enable_extensions = ["dollarmath"]
nbsphinx_execute = "never"
```

```{warning}
Do not add `sphinx.ext.mathjax`: Typst produces the MathML included in the final
HTML directly.
```

## Native Typst equations

Use Typst syntax between MyST's dollar delimiters. Inline equations can be
placed directly in a sentence:

```{myst-example}
The first $n$ positive integers satisfy
$sum_(k=1)^n k = (n(n+1))/2$.
```

Display equations work the same way:

```{myst-example}
$$
A = mat(1, 2; 3, 4)
quad det(A) = -2
$$
```

Typst features such as cases and text embedded in math remain available:

```{myst-example}
$$
abs(x) = cases(
  x & "if" x >= 0,
  -x & "if" x < 0,
)
$$
```

## reStructuredText input

The renderer also handles the standard reStructuredText math role and
directive. Their contents are still native Typst source:

```{eval-rst}
.. rst-example:: reStructuredText math

   Inline math uses :math:`sum_(k=1)^n k = (n(n+1))/2`.

   .. math::

      integral_0^infinity e^(-x^2) dif x = sqrt(pi) / 2
```

## Equation numbers and references

Attach a MyST label after a display equation. Sphinx owns the number, target,
and cross-reference while Typst renders the equation body.

```{myst-example}
$$
E = m c^2
$$ (mass-energy)

Equation {eq}`mass-energy` is rendered as native MathML and retains the normal
Sphinx permalink and reference behavior.
```

Labels can also be attached to reStructuredText math directives:

```{eval-rst}
.. rst-example::

   .. math::
      :label: mass-energy-rst

      E = m c^2

   Equation :eq:`mass-energy-rst` is rendered as native MathML and retains the
   normal Sphinx permalink and reference behavior.
```

## Shared definitions

The demonstration configuration defines an `expectation` helper in
`typst_math_preamble` in `conf.py`:

```python
typst_math_preamble = r"""
#expectation(X) = integral_(-infinity)^infinity x f(x) dif x
"""
```

It is available in every Markdown page and notebook:

```{myst-example}
$$
expectation(X) = integral_(-infinity)^infinity x f(x) dif x
$$
```

See [Typst package examples](package-examples.md) for `physica`, MiTeX, and
`quick-maths`, or open the [nbsphinx notebook](notebook.ipynb) to see the same
renderer used from Jupyter Markdown cells.

```{note}
The JupyterLab live preview normally uses MathJax and may not understand native
Typst syntax. The rendered notebook page produced by nbsphinx and Sphinx is the
authoritative preview for these equations.
```
