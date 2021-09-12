from autorepr import autorepr


class AB:
    def __init__(self, *, a, b):
        self.a = a
        self.b = b

    @autorepr
    def __repr__(self):
        return ("a", "b")


class CD(AB):
    def __init__(self, *, c, d, **kwargs):
        super().__init__(**kwargs)
        self.c = c
        self.d = d

    @autorepr
    def __repr__(self):
        return ("c", "d")


class EF(AB):
    def __init__(self, *, e, f, **kwargs):
        super().__init__(**kwargs)
        self.e = e
        self.f = f

    @autorepr
    def __repr__(self):
        return ("e", "f")


class Ignored:
    def __repr__(self):
        return "<Ignored has its own non-autorepr __repr__>"


class GH(EF, CD, Ignored):
    def __init__(self, *, g, h, **kwargs):
        super().__init__(**kwargs)
        self.g = g
        self.h = h

    @autorepr
    def __repr__(self):
        return ("g", "h")


def test_derived_repr():
    """Repr of a class hierarchy has attributes in reverse MRO"""
    obj = GH(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8)
    actual_repr = repr(obj)

    assert actual_repr == "GH(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8)"