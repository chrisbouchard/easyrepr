from autorepr import autorepr


class Base:
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar


class AngleStyleRepr(Base):
    @autorepr(style="<>")
    def __repr__(self):
        return ("foo", "bar")


class CallStyleRepr(Base):
    @autorepr(style="()")
    def __repr__(self):
        return ("foo", "bar")


def asserting_style_fn(instance, klass_name, attributes):
    instance.assert_fn(klass_name, attributes)
    return "Fancy repr string"


class FnStyleRepr(Base):
    def __init__(self, foo, bar, assert_fn):
        super().__init__(foo, bar)
        self.assert_fn = assert_fn

    @autorepr(style=asserting_style_fn)
    def __repr__(self):
        return ("foo", "bar")


def test_angle_style_repr():
    obj = AngleStyleRepr(1, 2)
    actual_repr = repr(obj)

    assert actual_repr == "<AngleStyleRepr foo=1 bar=2>"


def test_call_style_repr():
    obj = CallStyleRepr(1, 2)
    actual_repr = repr(obj)

    assert actual_repr == "CallStyleRepr(foo=1, bar=2)"


def test_fn_style_repr():
    def assert_fn(klass_name, attributes):
        assert klass_name == "FnStyleRepr"
        assert tuple(attributes) == (("foo", 1), ("bar", 2))

    obj = FnStyleRepr(1, 2, assert_fn)
    actual_repr = repr(obj)

    assert actual_repr == "Fancy repr string"
