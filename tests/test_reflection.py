from easyrepr.reflection import is_private, Mirror
import pytest


class A:
    def __init__(self):
        super().__init__()
        self.a1 = 1
        self._a2 = 2


class B:
    __slots__ = ("b1", "_b2")

    def __init__(self):
        super().__init__()
        self.b1 = 3
        self._b2 = 4


class C(B):
    __slots__ = ("c1", "_c2")

    def __init__(self):
        super().__init__()
        # These assignments are purposefully backwards.
        self._c2 = 6
        self.c1 = 5


class D(C, A):
    def __init__(self):
        super().__init__()
        self.d1 = 7
        self._d2 = 8


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
            D,
            {},
            [object, A, B, C, D],
            id="D with defaults",
        ),
        pytest.param(
            D,
            {"top_down": True},
            [object, A, B, C, D],
            id="D with top_down=True",
        ),
        pytest.param(
            D,
            {"top_down": False},
            [D, C, B, A, object],
            id="D with top_down=False",
        ),
        pytest.param(
            C,
            {},
            [object, B, C],
            id="C with defaults",
        ),
        pytest.param(
            C,
            {"top_down": True},
            [object, B, C],
            id="C with top_down=True",
        ),
        pytest.param(
            C,
            {"top_down": False},
            [C, B, object],
            id="C with top_down=False",
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
            D,
            {},
            ["b1", "c1", "a1", "d1"],
            id="D with defaults",
        ),
        pytest.param(
            D,
            {"hide_private": True},
            ["b1", "c1", "a1", "d1"],
            id="D with hide_private=True",
        ),
        pytest.param(
            D,
            {"hide_private": False},
            ["b1", "_b2", "c1", "_c2", "a1", "_a2", "d1", "_d2"],
            id="D with hide_private=False",
        ),
        pytest.param(
            D,
            {"hide_private": True, "top_down": False},
            ["c1", "b1", "a1", "d1"],
            id="D with hide_private=True, top_down=False",
        ),
        pytest.param(
            D,
            {"hide_private": False, "top_down": False},
            ["c1", "_c2", "b1", "_b2", "a1", "_a2", "d1", "_d2"],
            id="D with hide_private=False, top_down=False",
        ),
        pytest.param(
            C,
            {},
            ["b1", "c1"],
            id="C with defaults",
        ),
        pytest.param(
            C,
            {"hide_private": True},
            ["b1", "c1"],
            id="C with hide_private=True",
        ),
        pytest.param(
            C,
            {"hide_private": False},
            ["b1", "_b2", "c1", "_c2"],
            id="C with hide_private=False",
        ),
    ],
)
def test_mirror_reflect_attributes(test_class, mirror_args, expected_attributes):
    instance = test_class()
    mirror = Mirror(**mirror_args)

    # Result is just iterable; collect to a list for comparison.
    actual_attributes = list(mirror.reflect_attributes(instance))

    assert actual_attributes == expected_attributes
