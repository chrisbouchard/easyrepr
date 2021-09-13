import functools
import itertools
import types


__all__ = [
    "AutoRepr",
    "angle_style",
    "autorepr",
    "call_style",
    "format_attribute",
]


def autorepr(wrapped=None, **kwargs):
    """Decorator for an automatic ``__repr__`` method.

    This decorator wraps a function (which is available as ``__wrapped__``). The
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

    See :class:`AutoRepr` for a full description of the accepted arguments.

    This function may be called with all arguments (``wrapped`` and keyword
    arguments) up-front::

        autorepr(fn, style="<>")

    or it may be split.::

        autorepr(style="<>")(fn)

    This is to make it easier to use this function as a decorator.
    """

    def _autorepr(_wrapped):
        return AutoRepr(_wrapped, **kwargs)

    if wrapped is None:
        return _autorepr

    return _autorepr(wrapped)


class _AutoReprBootstrap(type):
    def __new__(cls, name, bases, dct):
        klass = super().__new__(cls, name, bases, dct)
        klass.__repr__ = klass(klass.__repr__, style="<>")
        return klass


class AutoRepr(metaclass=_AutoReprBootstrap):
    """Descriptor for an automatic ``__repr__`` method.

    This descriptor wraps a function (which is available as ``__wrapped__``).
    The wrapped function should return a description of the attributes that
    should be included in the repr.

    Valid attribute descriptions include:

    * ``None`` --- include all attributes of the instance (via :func:`vars`)

      *Note:* A function whose body is ``pass`` or ``...`` implicitly returns
      `None``.

    * An iterable containing zero or more of any of the following:

      * :class:`str` --- include the attribute with the given name
      * ``(key, value)`` --- include a virtual attribute
      * ``(value,)`` --- include a nameless virtual attribute

    The style of the repr string returned is determined by the ``style`` argument,
    which may be one of:

    * ``"()"`` --- use the "call" style, defined by ``call_style``::

          "Klass(foo=1, bar=2)"

    * ``"<>"`` --- use the "angle" style, defined by ``angle_style``::

          "<Klass foo=1 bar=2>"

    * :class:`~collections.abc.Callable` --- use a user-defined style function,
      which should accept three arguments: the object instance, the computed
      class name, and an iterable of attributes, which may be either
      ``(key, value)`` or ``(value,)``, as described above.
    """

    def __init__(self, wrapped, *, style=None):
        functools.update_wrapper(self, wrapped)
        self.style = style

    def __set_name__(self, owner, name):
        self.__objclass__ = owner

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return types.MethodType(self, instance)

    def __call__(self, instance):
        attributes = []
        style_fn = None

        for mro_type in reversed(type(instance).__mro__):
            repr_fn = getattr(mro_type, "__repr__", None)

            if not isinstance(repr_fn, AutoRepr):
                continue

            if repr_fn.style is not None and style_fn is None:
                style_fn = self._resolve_style(repr_fn.style)

            return_value = repr_fn.__wrapped__(instance)
            new_attributes = repr_fn._parse_repr_return_value(instance, return_value)
            attributes.extend(new_attributes)

        if style_fn is None:
            style_fn = self._resolve_style(self._default_style())

        klass_name = type(instance).__qualname__
        return style_fn(instance, klass_name, attributes)

    # This method is not annotated with @autorepr because it's not available
    # yet -- it needs *this* class to be defined. Instead, our metaclass,
    # AutoReprBootstrap, will replace this method with an AutoRepr instance.
    def __repr__(self):
        ...

    def _default_style(self):
        return call_style

    def _find_all_attributes(self, instance):
        return vars(instance).items()

    def _parse_repr_return_value(self, instance, return_value):
        if return_value is None:
            return self._find_all_attributes(instance)
        if isinstance(return_value, str):
            raise ValueError("for a string repr, remove @autorepr")

        attributes = []

        for item in return_value:
            if isinstance(item, str):
                attribute = (item, getattr(instance, item))
            else:
                attribute = item

                if len(attribute) < 1:
                    raise ValueError(f"empty attribute: {attribute}")
                if len(attribute) > 2:
                    raise ValueError(f"attribute has too many items: {attribute!r}")

            attributes.append(attribute)

        return attributes

    def _resolve_style(self, style):
        if style == "<>":
            return angle_style
        elif style == "()":
            return call_style
        return style


def angle_style(instance, klass_name, attributes):
    formatted_attributes = map(format_attribute, attributes)
    name_and_attributes = itertools.chain((klass_name,), formatted_attributes)
    joined_contents = " ".join(name_and_attributes)
    return f"<{joined_contents}>"


def call_style(instance, klass_name, attributes):
    formatted_attributes = map(format_attribute, attributes)
    joined_attributes = ", ".join(formatted_attributes)
    return f"{klass_name}({joined_attributes})"


def format_attribute(attribute):
    if len(attribute) == 1:
        (value,) = attribute
        return repr(value)

    key, value = attribute
    value_str = repr(value)

    if isinstance(key, str):
        key_str = key
    else:
        key_str = repr(key)

    return f"{key_str}={value_str}"
