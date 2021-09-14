from .descriptor import EasyRepr


__all__ = ["easyrepr"]


def easyrepr(wrapped=None, **kwargs):
    """Decorator for an automatic `__repr__` method.

    :param wrapped: the function to wrap

    See `.descriptor.EasyRepr` for a full description of the accepted
    keyword parameters.

    This decorator wraps a function (which is available as `__wrapped__`). The
    wrapped function should return a description of the attributes that should
    be included in the repr.

    .. doctest::

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

    This function may be called with all arguments up-front (wrapped function
    and keyword arguments) ::

        easyrepr(fn, style="<>")

    or the wrapped function may be provided in a second call ::

        easyrepr(style="<>")(fn)

    to make it easier to use this function as a decorator.
    """

    def _easyrepr(_wrapped):
        return EasyRepr(_wrapped, **kwargs)

    if wrapped is None:
        return _easyrepr

    return _easyrepr(wrapped)
