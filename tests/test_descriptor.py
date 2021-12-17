from easyrepr.descriptor import EasyRepr
import pytest


class TestCheckSignature:
    """Tests related to checking the wrapped function's signature."""

    def defaulted_self_function(self=None):
        ...

    def extra_defaulted_parameters_function(self, foo=None, *, bar=None):
        ...

    def goldilocks_function(self):
        ...

    def too_few_parameters_function():
        ...

    def too_many_parameters_function(self, foo, bar):
        ...

    @pytest.mark.parametrize("value", [None, 42, "hello world"])
    def test_noncallable_fails(self, value):
        """Easyrepr descriptor throws TypeError for non-callable values"""
        with pytest.raises(TypeError):
            EasyRepr(value)

    @pytest.mark.parametrize(
        "callable",
        [
            too_few_parameters_function,
            too_many_parameters_function,
        ],
    )
    def test_bad_signature_fails(self, callable):
        """Easyrepr descriptor throws TypeError for a callable with an incompatible
        signature.
        """
        with pytest.raises(TypeError):
            EasyRepr(callable)

    @pytest.mark.parametrize(
        "callable",
        [
            defaulted_self_function,
            extra_defaulted_parameters_function,
            goldilocks_function,
        ],
    )
    def test_good_signature_succeeds(self, callable):
        """Easyrepr descriptor succeeds for a callable with a compatible signature."""
        EasyRepr(callable)


class TestOverrideParam:
    """Tests related to the override parameter."""

    class Base:
        def __repr__(self):
            return [("base", "value")]

        __repr__ = EasyRepr(__repr__)

    class Derived(Base):
        def __repr__(self):
            return [("derived", "only")]

        __repr__ = EasyRepr(__repr__, override=True)

    def test_derived_override(self):
        instance = self.Derived()
        actual_repr = repr(instance)

        assert actual_repr == "TestOverrideParam.Derived(derived='only')"


class TestOverrideParamStyle:
    """Tests related to the override parameter."""

    class Base:
        def __repr__(self):
            return [("base", "value")]

        __repr__ = EasyRepr(__repr__, style=lambda x, y, z: "base style")

    class Derived(Base):
        def __repr__(self):
            return [("derived", "only")]

        __repr__ = EasyRepr(__repr__, override=True)

    def test_derived_override(self):
        instance = self.Derived()
        actual_repr = repr(instance)

        assert actual_repr == "TestOverrideParamStyle.Derived(derived='only')"
