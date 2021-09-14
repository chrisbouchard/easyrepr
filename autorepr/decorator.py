from .descriptor import AutoRepr


__all__ = ["autorepr"]


def autorepr(wrapped=None, **kwargs):
    """Decorator for an automatic `__repr__` method.

    :param wrapped: the function to wrap

    See `~.descriptor.AutoRepr` for a full description of the accepted
    keyword parameters.

    This decorator wraps a function (which is available as `__wrapped__`). The
    wrapped function should return a description of the attributes that should
    be included in the repr.

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

    This function may be called with all arguments up-front (wrapped function
    and keyword arguments) ::

        autorepr(fn, style="<>")

    or the wrapped function may be provided in a second call ::

        autorepr(style="<>")(fn)

    to make it easier to use this function as a decorator.
    """

    def _autorepr(_wrapped):
        return AutoRepr(_wrapped, **kwargs)

    if wrapped is None:
        return _autorepr

    return _autorepr(wrapped)
