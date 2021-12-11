from easyrepr import easyrepr


class SlotsBase:
    __slots__ = ("a", "b")

    @easyrepr
    def __repr__(self):
        ...


class SlotsDerived(SlotsBase):
    __slots__ = ("c", "d")


class DictDerived(SlotsDerived):
    pass


def test_slots_derived_full():
    """Repr for classes using only slots should handle ellipsis."""
    instance = SlotsDerived()
    instance.a = 1
    instance.b = 2
    instance.c = 3
    instance.d = 4

    actual_repr = repr(instance)

    assert actual_repr == "SlotsDerived(a=1, b=2, c=3, d=4)"


def test_slots_derived_partial():
    """Repr for classes using only slots should not include unset
    attributes.
    """
    instance = SlotsDerived()
    instance.a = 1
    instance.c = 3

    actual_repr = repr(instance)

    assert actual_repr == "SlotsDerived(a=1, c=3)"


def test_dict_derived_full():
    """Repr for classes using slots and dict should handle ellipsis."""
    instance = DictDerived()
    instance.a = 1
    instance.b = 2
    instance.c = 3
    instance.d = 4
    instance.e = 5
    instance.f = 6

    actual_repr = repr(instance)

    assert actual_repr == "DictDerived(a=1, b=2, c=3, d=4, e=5, f=6)"


def test_dict_derived_partial():
    """Repr for classes using slots and dict should not include unset
    attributes.
    """
    instance = DictDerived()
    instance.a = 1
    instance.c = 3
    instance.e = 5
    instance.f = 6

    actual_repr = repr(instance)

    assert actual_repr == "DictDerived(a=1, c=3, e=5, f=6)"
