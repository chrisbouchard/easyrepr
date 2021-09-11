import types


__all__ = ["autorepr"]


def autorepr(attributes_fn, *, style=None):
    return AutoRepr(attributes_fn, style)


def angle_style(klass_name, attributes):
    formatted_args = " ".join(f"{k}={v!r}" for k, v in attributes)
    if formatted_args:
        formatted_args = " " + formatted_args
    return f"<{klass_name}{formatted_args}>"


def call_style(klass_name, attributes):
    formatted_args = ", ".join(f"{k}={v!r}" for k, v in attributes)
    return f"{klass_name}({formatted_args})"


class AutoRepr:
    default_style = call_style

    def __init__(self, attributes_fn, style):
        self.attributes_fn = attributes_fn
        self.style = style

        self.__doc__ = attributes_fn.__doc__
        self.__module__ = attributes_fn.__module__
        self.__name__ = attributes_fn.__name__
        self.__qualname__ = attributes_fn.__qualname__

    def __set_name__(self, owner, name):
        self.__objclass__ = owner

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return types.MethodType(self, instance)

    def __call__(self, instance):
        attributes = []
        style_fn = None

        for mro_type in type(instance).__mro__:
            repr_fn = getattr(mro_type, "__repr__", None)

            if not isinstance(super_repr, AutoRepr):
                continue

            if repr_fn.style is not None and style_fn is None:
                style_fn = self._resolve_style(repr_fn.style)

            new_names = repr_fn.attributes_fn(instance)
            attributes[0:0] = ((name, getattr(instance, name)) for name in new_names)

        if style_fn is None:
            style_fn = self._resolve_style(self.default_style)

        klass_name = type(instance).__qualname__
        return style_fn(klass_name, attributes)

    def _resolve_style(self, style):
        if style == "<>":
            return angle_style
        elif style == "()":
            return call_style
        return style
