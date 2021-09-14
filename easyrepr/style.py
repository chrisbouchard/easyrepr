import itertools


__all__ = ["angle_style", "call_style", "format_attribute"]


def angle_style(instance, klass_name, attributes):
    """Style function for an angular repr in the style of `object`.

    :param instance: the object whose repr is being formatted
    :param klass_name: the class name that should be displayed
    :param attributes: the sequence of attribute tuples
    :returns: the styled repr string

    .. doctest::

       >>> angle_style(obj, "Klass", [("foo", 1), ("bar", 2)])
       '<Klass foo=1 bar=2>'
    """

    formatted_attributes = map(format_attribute, attributes)
    name_and_attributes = itertools.chain((klass_name,), formatted_attributes)
    joined_contents = " ".join(name_and_attributes)

    return f"<{joined_contents}>"


def call_style(instance, klass_name, attributes):
    """Style function for an angular repr in the style of a constructor call.

    :param instance: the object whose repr is being formatted
    :param klass_name: the class name that should be displayed
    :param attributes: the sequence of attribute tuples
    :returns: the styled repr string

    .. doctest::

       >>> call_style(obj, "Klass", [("foo", 1), ("bar", 2)])
       'Klass(foo=1, bar=2)'
    """

    formatted_attributes = map(format_attribute, attributes)
    joined_attributes = ", ".join(formatted_attributes)

    return f"{klass_name}({joined_attributes})"


def format_attribute(attribute):
    """Format a tuple describing an attribute.

    :param attribute: attribute tuple, which may be either ``(key, value)`` or
      ``(value,)``.
    :return: the formatted string

    If given, `key` is either formatted as itself, if it's a `str`, or else as
    ``repr(key)``, and is separated from `value` by an equal sign ("=").
    `value` is always formatted as ``repr(value)``.
    """
    if len(attribute) == 1:
        (value,) = attribute
        return repr(value)

    key, value = attribute
    value_str = repr(value)

    if isinstance(key, str):
        key_str = key
    else:
        key_str = repr(key)

    return f"{key_str}={value_str}"
