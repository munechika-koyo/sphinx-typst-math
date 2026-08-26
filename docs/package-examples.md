# Typst package examples

Typst Universe packages can be loaded for every equation with
`typst_math_imports`, or imported selectively in `typst_math_preamble`. This
demonstration uses both approaches:

```python
typst_math_imports = [
    "@preview/physica:0.9.8",
]

typst_math_preamble = r"""
#import "@preview/mitex:0.2.7": mi
#import "@preview/quick-maths:0.2.1": shorthands

#show: shorthands.with(
  ($+-$, $plus.minus$),
  ($|-$, math.tack),
)
"""
```

Package references include an exact version so documentation builds remain
reproducible. On the first build, Typst downloads missing packages and stores
them in its local package cache.

## physica

[`physica`](https://typst.app/universe/package/physica/) provides notation for
physics, engineering, and higher mathematics. Because it is listed in
`typst_math_imports`, its exported functions can be used directly in math
source.

A mixed third-order partial derivative:

```{myst-example}
$$
pdv(f, x, y, [1, 2])
$$
```

Vector calculus and tensor notation:

```{myst-example}
$$
curl (grad f) = 0
quad tensor(T, -mu, +nu)
$$
```

## MiTeX

[`MiTeX`](https://typst.app/universe/package/mitex/) is useful while migrating
existing LaTeX equations. Here, its `mi` function parses the raw LaTeX string,
then Typst emits the resulting MathML:

```{myst-example}
$$
#mi(raw("\\frac{1}{2}\\sum_{k=1}^{n} k"))
$$
```

This is an opt-in compatibility bridge. Native Typst source remains simpler for
new equations and exposes the full Typst math language directly.

## quick-maths

[`quick-maths`](https://typst.app/universe/package/quick-maths/) defines project
shorthands. The preamble maps `+-` to a plus-minus sign and `|-` to a turnstile,
so all documentation pages share the same notation:

```{myst-example}
$$
x^2 = 9 quad <==> quad x = +-3
$$
```

```{myst-example}
$$
A or B |- A
$$
```

## Local packages

Local `.typ` files work too. Paths are resolved from the Sphinx source
directory (`docs/` in this project):

```python
typst_math_imports = [
    "_typst/project-math.typ",
]
```

Use a selective import in the preamble when importing everything would create
name collisions:

```python
typst_math_preamble = r"""
#import "_typst/project-math.typ": norm, inner-product
"""
```
