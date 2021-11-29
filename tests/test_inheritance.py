from easyrepr import easyrepr


class AB:
    def __init__(self, *, a, b):
        self.a = a
        self.b = b

    @easyrepr
    def __repr__(self):
        return ("a", "b")


class CD(AB):
    def __init__(self, *, c, d, **kwargs):
        super().__init__(**kwargs)
        self.c = c
        self.d = d

    @easyrepr
    def __repr__(self):
        return ("c", "d")


class EF(AB):
    def __init__(self, *, e, f, **kwargs):
        super().__init__(**kwargs)
        self.e = e
        self.f = f

    @easyrepr
    def __repr__(self):
        return ("e", "f")


class Ignored:
    def __repr__(self):
        return "<Ignored has its own non-easyrepr __repr__>"


class GH(EF, CD, Ignored):
    def __init__(self, *, g, h, **kwargs):
        super().__init__(**kwargs)
        self.g = g
        self.h = h

    @easyrepr
    def __repr__(self):
        return ("g", "h")


class BaseWithEllipsis:
    def __init__(self, *, a, b):
        self.a = a
        self.b = b

    @easyrepr
    def __repr__(self):
        ...


class EmptyDerived(BaseWithEllipsis):
    pass


class BaseWithDifferentMethodName:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @easyrepr
    def other_method(self):
        return ("a", "b")


class DerivedWithDifferentMethodName(BaseWithDifferentMethodName):
    def __init__(self, a, b, c, d):
        super().__init__(a, b)
        self.c = c
        self.d = d

    @easyrepr
    def other_method(self):
        return ("c", "d")


def test_derived_repr():
    """Repr of a class hierarchy has attributes in reverse MRO"""
    obj = GH(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8)
    actual_repr = repr(obj)

    assert actual_repr == "GH(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8)"


def test_derived_ellipsis():
    """Repr of a class does not have duplicated attributes with inheritance"""
    obj = EmptyDerived(a=1, b=2)
    actual_repr = repr(obj)

    assert actual_repr == "EmptyDerived(a=1, b=2)"


def test_inherited_different_method_name():
    """Class using inheritance with a method name other than __repr__"""
    obj = DerivedWithDifferentMethodName(a=1, b=2, c=3, d=4)
    actual_repr = obj.other_method()

    assert actual_repr == "DerivedWithDifferentMethodName(a=1, b=2, c=3, d=4)"
