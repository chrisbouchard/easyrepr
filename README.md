# easyrepr

[![PyPI version][pypi-badge]][pypi-link]
[![CircleCI][circleci-badge]][circleci-link]
[![Read the Docs][rtd-badge]][rtd-link]

Python decorator to automatically generate repr strings

[pypi-badge]: https://badge.fury.io/py/easyrepr.svg
[pypi-link]: https://pypi.org/project/easyrepr/
[circleci-badge]: https://circleci.com/gh/chrisbouchard/easyrepr/tree/main.svg?style=shield
[circleci-link]: https://circleci.com/gh/chrisbouchard/easyrepr/tree/main
[rtd-badge]: https://readthedocs.org/projects/easyrepr/badge/
[rtd-link]: https://easyrepr.readthedocs.io/en/latest/

## Example

```pycon
>>> class UseEasyRepr:
...     def __init__(self, foo, bar):
...         self.foo = foo
...         self.bar = bar
...     @easyrepr
...     def __repr__(self):
...         ...
...
>>> x = UseEasyRepr(1, 2)
>>> repr(x)
'UseEasyRepr(foo=1, bar=2)'
```

## Installation

```console
$ pip install easyrepr
```
