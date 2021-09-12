import functools
import itertools
import types


__all__ = ["autorepr"]


def autorepr(wrapped=None, **kwargs):
    def _autorepr(_wrapped):
        return AutoRepr(_wrapped, **kwargs)

    if wrapped is None:
        return _autorepr

    return _autorepr(wrapped)


class AutoRepr:
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
