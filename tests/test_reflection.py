from easyrepr.reflection import is_private, Mirror
import pytest


class DictBase:
    def __init__(self):
        super().__init__()
        self.a1 = 1
        self._a2 = 2


class SlotsBase:
    __slots__ = ("b1", "_b2")

    def __init__(self):
        super().__init__()
        self.b1 = 3
        self._b2 = 4


class SlotsDerived(SlotsBase):
    __slots__ = ("c1", "_c2")

    def __init__(self):
        super().__init__()
        # These assignments are intentionally backwards.
        self._c2 = 6
        self.c1 = 5


class DictAndSlots(SlotsDerived, DictBase):
    def __init__(self):
        super().__init__()
        self.d1 = 7
        self._d2 = 8


class SlotsOneAttrUnset(SlotsDerived):
    __slots__ = ("e1", "e2")

    def __init__(self):
        super().__init__()
        self.e1 = 9
        # e2 intentionally left unset.


@pytest.mark.parametrize(
    ("attribute", "value"),
    [
        ("abc", False),
        ("a_b_c", False),
        ("abc_", False),
        ("_abc", True),
        ("__abc", True),
        ("foo_bar", False),
        ("_foo_bar", True),
        ("__foo_bar", True),
        ("_", True),
    ],
)
def test_is_private(attribute, value):
    assert is_private(attribute) is value


@pytest.mark.parametrize(
    ("test_class", "mirror_args", "expected_classes"),
    [
        pytest.param(
            DictAndSlots,
            {},
            [object, DictBase, SlotsBase, SlotsDerived, DictAndSlots],
            id="DictAndSlots with defaults",
        ),
        pytest.param(
            DictAndSlots,
            {"top_down": True},
            [object, DictBase, SlotsBase, SlotsDerived, DictAndSlots],
            id="DictAndSlots with top_down=True",
        ),
        pytest.param(
            DictAndSlots,
            {"top_down": False},
            [DictAndSlots, SlotsDerived, SlotsBase, DictBase, object],
            id="DictAndSlots with top_down=False",
        ),
        pytest.param(
            SlotsDerived,
            {},
            [object, SlotsBase, SlotsDerived],
            id="SlotsDerived with defaults",
        ),
        pytest.param(
            SlotsDerived,
            {"top_down": True},
            [object, SlotsBase, SlotsDerived],
            id="SlotsDerived with top_down=True",
        ),
        pytest.param(
            SlotsDerived,
            {"top_down": False},
            [SlotsDerived, SlotsBase, object],
            id="SlotsDerived with top_down=False",
        ),
    ],
)
def test_mirror_reflect_classes(test_class, mirror_args, expected_classes):
    instance = test_class()
    mirror = Mirror(**mirror_args)

    # Result is just iterable; collect to a list for comparison.
    actual_classes = list(mirror.reflect_classes(instance))

    assert actual_classes == expected_classes


@pytest.mark.parametrize(
    ("test_class", "mirror_args", "expected_attributes"),
    [
        pytest.param(
            DictAndSlots,
            {},
            ["b1", "c1", "a1", "d1"],
            id="DictAndSlots with defaults",
        ),
        pytest.param(
            DictAndSlots,
            {"hide_private": True},
            ["b1", "c1", "a1", "d1"],
            id="DictAndSlots with hide_private=True",
        ),
        pytest.param(
            DictAndSlots,
            {"hide_private": False},
            ["b1", "_b2", "c1", "_c2", "a1", "_a2", "d1", "_d2"],
            id="DictAndSlots with hide_private=False",
        ),
        pytest.param(
            DictAndSlots,
            {"hide_private": True, "top_down": False},
            ["c1", "b1", "a1", "d1"],
            id="DictAndSlots with hide_private=True, top_down=False",
        ),
        pytest.param(
            DictAndSlots,
            {"hide_private": False, "top_down": False},
            ["c1", "_c2", "b1", "_b2", "a1", "_a2", "d1", "_d2"],
            id="DictAndSlots with hide_private=False, top_down=False",
        ),
        pytest.param(
            SlotsDerived,
            {},
            ["b1", "c1"],
            id="SlotsDerived with defaults",
        ),
        pytest.param(
            SlotsDerived,
            {"hide_private": True},
            ["b1", "c1"],
            id="SlotsDerived with hide_private=True",
        ),
        pytest.param(
            SlotsDerived,
            {"hide_private": False},
            ["b1", "_b2", "c1", "_c2"],
            id="SlotsDerived with hide_private=False",
        ),
        pytest.param(
            SlotsOneAttrUnset,
            {},
            ["b1", "c1", "e1"],
            id="SlotsOneAttrUnset with defaults",
        ),
    ],
)
def test_mirror_reflect_attributes(test_class, mirror_args, expected_attributes):
    instance = test_class()
    mirror = Mirror(**mirror_args)

    # Result is just iterable; collect to a list for comparison.
    actual_attributes = list(mirror.reflect_attributes(instance))

    assert actual_attributes == expected_attributes
