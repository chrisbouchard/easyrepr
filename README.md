# autorepr

[![Read the Docs][rtd-badge]][rtd-link]

Python decorator to automatically generate repr strings

[rtd-badge]: https://readthedocs.org/projects/pip/badge/
[rtd-link]: https://autorepr.readthedocs.io/en/latest/

## Example

```pycon
>>> class UseAutoRepr:
...     def __init__(self, foo, bar):
...         self.foo = foo
...         self.bar = bar
...     @autorepr
...     def __repr__(self):
...         ...
...
>>> x = UseAutoRepr(1, 2)
>>> repr(x)
'UseAutoRepr(foo=1, bar=2)'
```

## Installation

```console
$ pip install autorepr
```
