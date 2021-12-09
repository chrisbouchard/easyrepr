__all__ = ["is_private", "Mirror"]


def is_private(attribute):
    """Return whether an attribute is private."""
    return attribute.startswith("_")


class Mirror:
    """Class to access attributes via reflection.

    :param hide_private: do not include private (according to
      :any:`is_private`) attributes when reflecting attributes. Default is
      `True`.
    """

    def __init__(self, hide_private=True):
        self.hide_private = hide_private

    def reflect_classes(self, instance, bottom_up=False):
        """Return all classes in the method resolution order (MRO) for the
        given instance's type.

        :param instance: the object whose classes should be reflected
        :param bottom_up: if `True`, return classes from bottom (most derived)
          to top (most base, usually :any:`object`); otherwise from top to
          bottom. Default is `False` (top to bottom).
        """
        classes_bottom_up = type(instance).__mro__

        if bottom_up:
            return classes_bottom_up

        return reversed(classes_bottom_up)

    def reflect_attributes(self, instance):
        """Return all visible attributes of the given instance.

        :param instance: the object whose attributes should be reflected
        """
        attributes = []

        for klass in self.reflect_classes(instance):
            if hasattr(klass, "__slots__"):
                attributes.extend(self._filter_private_attributes(klass.__slots__))

        if hasattr(instance, "__dict__"):
            attributes.extend(self._filter_private_attributes(instance.__dict__.keys()))

        return attributes

    def _filter_private_attributes(self, candidate_attributes):
        if not self.hide_private:
            return candidate_attributes

        return (
            attribute for attribute in candidate_attributes if not is_private(attribute)
        )

    def __repr__(self):
        # No easy way to get EasyRepr in here. "I guide others to a treasure I
        # cannot possess."
        return f"Mirror(skip_private={self.hide_private})"
