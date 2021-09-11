import types


__all__ = ['AutoRepr', 'autorepr']


def autorepr(attributes_fn):
    return AutoRepr(attributes_fn)


class AutoRepr:
    def __init__(self, attributes_fn):
        self.attributes_fn = attributes_fn
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
        super_types = type(instance).__mro__
        attributes = []

        for super_type in super_types:
            super_repr = super_type.__repr__

            if not isinstance(super_repr, AutoRepr):
                continue

            attributes[0:0] = super_repr.attributes_fn(instance)

        klass = type(instance).__qualname__
        args = (f"{attr}={getattr(instance, attr)}" for attr in attributes)

        joined_args = ", ".join(args)
        return f"{klass}({joined_args})"
