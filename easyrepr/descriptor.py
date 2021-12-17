import functools
import inspect
import types
from collections.abc import Sequence

from .reflection import Mirror
from .style import angle_style, call_style


__all__ = ["EasyRepr"]


class _EasyReprBootstrap(type):
    """Use the EasyRepr to repr the EasyRepr.

    We'd like to use EasyRepr for its own __repr__ implementation, but that
    runs into a problem, because EasyRepr isn't available for use while its
    class is still being defined. So this metaclass exists solely to wire up
    EasyRepr.__repr__ after the fact.
    """

    def __new__(cls, name, bases, dct):
        klass = super().__new__(cls, name, bases, dct)

        # Since we're adding this descriptor after klass was created, we're
        # responsible for calling __set_name__ manually.
        repr_descriptor = klass(klass.__repr__)
        klass.__repr__ = repr_descriptor
        repr_descriptor.__set_name__(klass, "__repr__")

        return klass


class EasyRepr(metaclass=_EasyReprBootstrap):
    """Descriptor for an automatic `__repr__` method.

    :param wrapped: the function to wrap
    :param override: completely replace ancestor methods rather than
      concatenating to them. Default is `False`.
    :param skip_private: skip private attributes --- i.e., those whose names
      start with an underscore ("_") --- when finding attributes for `None` or
      `Ellipsis`. Default is `True`.
    :param style: the style to use. Default is `None`.

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

    * `None` --- inherit style from super class, or else default to "call"
      style. (This is the default.)
    * ``"()"`` --- use the "call" style, defined by :func:`.style.call_style`::

          "Klass(foo=1, bar=2)"

    * ``"<>"`` --- use the "angle" style, defined by :func:`.style.angle_style`::

          "<Klass foo=1 bar=2>"

    * `~collections.abc.Callable` --- use a user-defined style function, which
      should accept three parameters: the object instance, the computed class
      name, and an iterable of attributes, which may be either ``(key, value)``
      or ``(value,)``, as described above.
    """

    def __init__(self, wrapped, *, override=False, skip_private=True, style=None):
        self._check_wrapped(wrapped)
        functools.update_wrapper(self, wrapped)

        self.override = override
        self.style = style

        self._mirror = Mirror(skip_private)

    def __set_name__(self, owner, name):
        self.__objclass__ = owner
        self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return types.MethodType(self, instance)

    def __call__(self, instance):
        attributes = []
        style_fn = None

        if self.override:
            search_classes = (type(instance),)
        else:
            search_classes = self._mirror.reflect_classes(instance)

        for mro_type in search_classes:
            repr_fn = mro_type.__dict__.get(self._name, None)

            if not isinstance(repr_fn, EasyRepr):
                continue

            if repr_fn.style is not None:
                style_fn = self._resolve_style(repr_fn.style)

            return_value = repr_fn.__wrapped__(instance)
            new_attributes = repr_fn._expand_repr_return_value(instance, return_value)
            attributes.extend(new_attributes)

        attributes = self._process_attribute_sequence(instance, attributes)

        if style_fn is None:
            style_fn = self._resolve_style(self._default_style())

        klass_name = type(instance).__qualname__
        return style_fn(instance, klass_name, attributes)

    # This method is not annotated with @easyrepr because it's not available
    # yet -- it needs *this* class to be defined. Instead, our metaclass,
    # EasyReprBootstrap, will replace this method with an EasyRepr instance.
    def __repr__(self):
        return (("wrapped", self.__wrapped__), ...)

    def _check_wrapped(self, wrapped):
        try:
            signature = inspect.signature(wrapped)
        except TypeError:
            raise TypeError("wrapped value is not callable")

        try:
            signature.bind(None)
        except TypeError:
            raise TypeError(
                "wrapped function is not callable with one positional argument "
                "(self)"
            )

    def _default_style(self):
        return call_style

    def _expand_repr_return_value(self, instance, return_value):
        if return_value is None:
            return self._mirror.reflect_attributes(instance)
        if isinstance(return_value, str):
            raise ValueError("for a string repr, remove @easyrepr or EasyRepr")
        if not isinstance(return_value, Sequence):
            raise ValueError(
                f"return value is not a sequence or None: {return_value!r}"
            )

        attributes = []

        for item in return_value:
            if isinstance(item, str):
                attributes.append(item)
            elif isinstance(item, Sequence):
                if len(item) < 1:
                    raise ValueError(f"empty attribute: {item!r}")
                if len(item) > 2:
                    raise ValueError(f"attribute has too many items: {item!r}")

                attributes.append(tuple(item))
            elif item == Ellipsis:
                attributes.extend(self._mirror.reflect_attributes(instance))
            else:
                raise ValueError(
                    f"attribute is not a string, sequence, or ellipsis: {item!r}"
                )

        return attributes

    def _process_attribute_sequence(self, instance, attributes):
        processed_attributes = []

        for attribute in attributes:
            if isinstance(attribute, str):
                processed_attributes.append((attribute, getattr(instance, attribute)))
            else:
                processed_attributes.append(attribute)

        return processed_attributes

    def _resolve_style(self, style):
        if style == "<>":
            return angle_style
        elif style == "()":
            return call_style
        return style
