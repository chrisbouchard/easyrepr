import functools
import types
from collections.abc import Sequence

from .style import angle_style, call_style


__all__ = ["EasyRepr"]


class _EasyReprBootstrap(type):
    def __new__(cls, name, bases, dct):
        klass = super().__new__(cls, name, bases, dct)
        klass.__repr__ = klass(klass.__repr__)
        return klass


class EasyRepr(metaclass=_EasyReprBootstrap):
    """Descriptor for an automatic `__repr__` method.

    :param wrapped: the function to wrap
    :param skip_private: skip private attributes --- i.e., those whose names
      start with an underscore ("_") --- when finding attributes for `None` or
      `Ellipsis`.
    :param style: the style to use

    :ivar __wrapped__: the wrapped function

    This descriptor wraps a function (which is available as `__wrapped__`). The
    wrapped function should return a description of the attributes that should
    be included in the repr.

    Valid attribute descriptions include:

    * `None` --- include all attributes of the instance (via `vars`)

      .. note:: A function whose body is :keyword:`pass` or `Ellipsis`
         (:any:`...`) implicitly returns `None`.

    * An iterable containing zero or more of any of the following:

      * `str` --- include the attribute with the given name
      * ``(key, value)`` --- include a virtual attribute
      * ``(value,)`` --- include a nameless virtual attribute
      * `Ellipsis` (:any:`...`) --- include all attributes of the instance (via
        :func:`vars`)

    The style of the repr string returned is determined by the `style`
    parameter, which may be one of:

    * ``"()"`` --- use the "call" style, defined by :func:`.style.call_style`::

          "Klass(foo=1, bar=2)"

    * ``"<>"`` --- use the "angle" style, defined by :func:`.style.angle_style`::

          "<Klass foo=1 bar=2>"

    * `~collections.abc.Callable` --- use a user-defined style function, which
      should accept three parameters: the object instance, the computed class
      name, and an iterable of attributes, which may be either ``(key, value)``
      or ``(value,)``, as described above.
    """

    def __init__(self, wrapped, *, skip_private=True, style=None):
        functools.update_wrapper(self, wrapped)
        self.skip_private = skip_private
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

            if not isinstance(repr_fn, EasyRepr):
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

    # This method is not annotated with @easyrepr because it's not available
    # yet -- it needs *this* class to be defined. Instead, our metaclass,
    # EasyReprBootstrap, will replace this method with an EasyRepr instance.
    def __repr__(self):
        return (("wrapped", self.__wrapped__), ...)

    def _default_style(self):
        return call_style

    def _find_all_attributes(self, instance):
        attributes = vars(instance).items()

        if self.skip_private:
            attributes = (
                (name, value) for name, value in attributes if not name.startswith("_")
            )

        return attributes

    def _parse_repr_return_value(self, instance, return_value):
        if return_value is None:
            return self._find_all_attributes(instance)
        if isinstance(return_value, str):
            raise ValueError("for a string repr, remove @easyrepr or EasyRepr")

        attributes = []

        for item in return_value:
            if isinstance(item, str):
                attributes.append(
                    (item, getattr(instance, item)),
                )
            elif item == Ellipsis:
                attributes.extend(self._find_all_attributes(instance))
            else:
                if not isinstance(item, Sequence):
                    raise ValueError(f"attribute is not a sequence: {item}")
                if len(item) < 1:
                    raise ValueError(f"empty attribute: {item}")
                if len(item) > 2:
                    raise ValueError(f"attribute has too many items: {item!r}")

                attributes.append(tuple(item))

        return attributes

    def _resolve_style(self, style):
        if style == "<>":
            return angle_style
        elif style == "()":
            return call_style
        return style
