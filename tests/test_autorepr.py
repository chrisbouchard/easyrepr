from autorepr import autorepr


class BasicRepr:
    """Basic class using an unconfigured autorepr for its __repr__"""

    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar

    # We ignore type errors and the undefined name "Return" because this is
    # just for testing.
    @autorepr
    def __repr__(self) -> "Return":  # type: ignore # noqa: F821
        """Docstring for BasicRepr.__repr__"""
        return ("foo", "bar")


class Named:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<object named {self.name}>"


def test_basic_repr_free():
    """Free repr function with simple arguments returns repr"""
    obj = BasicRepr(1, 2)
    actual_repr = repr(obj)

    assert actual_repr == "BasicRepr(foo=1, bar=2)"


def test_basic_repr_instance_binding():
    """Call through instance with simple arguments returns repr"""
    obj = BasicRepr(1, 2)
    actual_repr = obj.__repr__()

    assert actual_repr == "BasicRepr(foo=1, bar=2)"


def test_basic_repr_direct_binding():
    """Direct call with simple arguments returns repr"""
    obj = BasicRepr(1, 2)
    actual_repr = BasicRepr.__repr__(obj)

    assert actual_repr == "BasicRepr(foo=1, bar=2)"


def test_basic_repr_with_objects():
    """Call with object arguments calls repr on arguments"""
    foo = Named("foo")
    bar = Named("bar")
    obj = BasicRepr(foo, bar)
    actual_repr = repr(obj)

    assert actual_repr == "BasicRepr(foo=<object named foo>, bar=<object named bar>)"


def test_autorepr_preserves_relevant_attributes():
    assert BasicRepr.__repr__.__module__ == "tests.test_autorepr"
    assert BasicRepr.__repr__.__name__ == "__repr__"
    assert BasicRepr.__repr__.__qualname__ == "BasicRepr.__repr__"
    assert BasicRepr.__repr__.__doc__ == "Docstring for BasicRepr.__repr__"
    assert BasicRepr.__repr__.__annotations__ == {"return": "Return"}
