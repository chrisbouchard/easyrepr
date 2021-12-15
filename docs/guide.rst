==========
User Guide
==========


Installation
============

From PyPI
---------

Easyrepr is `available on PyPI`_, so the easiest method of installation is via
``pip``.

.. code-block:: console
   :caption: Install from PyPI

   $ pip install easyrepr

.. _available on PyPI: https://pypi.org/project/easyrepr/

From Source
-----------

For development, you can check out the source `from GitHub`_ and create a
virtual environment `using Poetry`_.

.. code-block:: console
   :caption: Install from source

   $ git clone https://github.com/chrisbouchard/easyrepr.git
   $ cd easyrepr
   $ poetry install

.. _from GitHub: https://github.com/chrisbouchard/easyrepr
.. _using Poetry: https://python-poetry.org/


Using easyrepr
==============

The simplest way to use easyrepr is to decorate your :obj:`__repr__` method
with the :func:`~easyrepr.easyrepr` decorator and return :obj:`None`, e.g.,
with an empty function body. This will cause easyrepr to automatically generate
a repr based on :func:`vars` (skipping private attributes).

.. code-block:: pycon
   :caption: Repr with all public attributes

   >>> from easyrepr import easyrepr
   ...
   >>> class UseEasyRepr:
   ...     def __init__(self, foo, bar):
   ...         self.foo = foo
   ...         self.bar = bar
   ...
   ...     @easyrepr
   ...     def __repr__(self):
   ...         ...
   ...
   >>> x = UseEasyRepr(1, 2)
   >>> repr(x)
   'UseEasyRepr(foo=1, bar=2)'

Specifying Attributes by Name
-----------------------------

Your :obj:`__repr__` method can return a sequence to make easyrepr display
specific attributes in the generated repr. If an item in the sequence is a
:obj:`str`, easyrepr will include the attribute with that name.

.. code-block:: pycon
   :caption: Repr with listed attributes

   >>> from easyrepr import easyrepr
   ...
   >>> class UseEasyRepr:
   ...     def __init__(self, foo, bar, baz):
   ...         self.foo = foo
   ...         self.bar = bar
   ...         self.baz = baz
   ...
   ...     @easyrepr
   ...     def __repr__(self):
   ...         return ("foo", "baz")
   ...
   >>> x = UseEasyRepr(1, 2, 3)
   >>> repr(x)
   'UseEasyRepr(foo=1, baz=3)'

Virtual Attributes
------------------

If an item in the sequence is a :obj:`tuple` with two elements, easyrepr will
interpret it as a "virtual attribute", which lets you provide a name and value
directly. The virtual attribute does *not* have to correspond to an actual
attribute of the object.

.. code-block:: pycon
   :caption: Repr with a virtual attribute

   >>> from easyrepr import easyrepr
   ...
   >>> class UseEasyRepr:
   ...     def __init__(self, foo, bar):
   ...         self.foo = foo
   ...         self.bar = bar
   ...
   ...     @easyrepr
   ...     def __repr__(self):
   ...         return ("foo", ("virtual", 42))
   ...
   >>> x = UseEasyRepr(1, 2)
   >>> repr(x)
   'UseEasyRepr(foo=1, virtual=42)'

Nameless Virtual Attributes
---------------------------

If an item in the sequence is a :obj:`tuple` with one element, easyrepr will
interpret it as a *nameless* virtual attribute. The value will be included in
the generated repr directly.

.. code-block:: pycon
   :caption: Repr with a nameless virtual attribute

   >>> from easyrepr import easyrepr
   ...
   >>> class UseEasyRepr:
   ...     def __init__(self, foo, bar):
   ...         self.foo = foo
   ...         self.bar = bar
   ...
   ...     @easyrepr
   ...     def __repr__(self):
   ...         return ("foo", ("nameless",))
   ...
   >>> x = UseEasyRepr(1, 2)
   >>> repr(x)
   "UseEasyRepr(foo=1, 'nameless')"

Including All Public Attributes
-------------------------------

If an item in the sequence is :obj:`Ellipsis` (also spelled :any:`...`),
easyrepr will include all attributes from :func:`vars`, just like when
:obj:`__repr__` returned :obj:`None` above. By default, easyrepr will skip
private attributes --- attributes whose names start with underscore ("_").

.. note::

   Multiple instances of :obj:`Ellipsis` will result in the attributes
   being duplicated. It's essentially expanded in-place.

.. code-block:: pycon
   :caption: Repr with a virtual attribute

   >>> from easyrepr import easyrepr
   ...
   >>> class UseEasyRepr:
   ...     def __init__(self, foo, bar, baz):
   ...         self.foo = foo
   ...         self.bar = bar
   ...         self._baz = baz
   ...
   ...     @easyrepr
   ...     def __repr__(self):
   ...         return (..., ("virtual", 42))
   ...
   >>> x = UseEasyRepr(1, 2, 3)
   >>> repr(x)
   'UseEasyRepr(foo=1, bar=2, virtual=42)'

Including Private Attributes
----------------------------

To make easyrepr include private attributes for :obj:`Ellipsis` (and when
:obj:`__repr__` returns :obj:`None`), you can pass ``skip_private=False`` to
:func:`~easyrepr.easyrepr`.

.. note::

   The :obj:`~easyrepr.easyrepr.skip_private` argument only affects how
   :obj:`None` and :obj:`Ellipsis` are handled. Attributes specified as strings
   or tuples are always included.

.. code-block:: pycon
   :caption: Repr with a virtual attribute

   >>> from easyrepr import easyrepr
   ...
   >>> class UseEasyRepr:
   ...     def __init__(self, foo, bar, baz):
   ...         self.foo = foo
   ...         self.bar = bar
   ...         self._baz = baz
   ...
   ...     @easyrepr(skip_private=False)
   ...     def __repr__(self):
   ...         return (..., ("virtual", 42))
   ...
   >>> x = UseEasyRepr(1, 2, 3)
   >>> repr(x)
   'UseEasyRepr(foo=1, bar=2, _baz=3, virtual=42)'


Styles
======

You can use a style to change how easyrepr formats the repr it generates.

.. _"Call" Style:

"Call" Style
------------

The default style is "call" style, defined by
:func:`easyrepr.style.call_style`, which formats the repr similar to a
constructor call.

To set the style, use the :obj:`~easyrepr.easyrepr.style` parameter to the
:func:`~easyrepr.easyrepr` decorator. E.g., to explicitly set "call" style,
pass ``style="()"`` (a string of open and close parentheses).

.. code-block:: pycon
   :caption: Repr using explicit "call" style

   >>> from easyrepr import easyrepr
   ...
   >>> class UseEasyRepr:
   ...     def __init__(self, foo, bar):
   ...         self.foo = foo
   ...         self.bar = bar
   ...
   ...     @easyrepr(style="()")
   ...     def __repr__(self):
   ...         ...
   ...
   >>> x = UseEasyRepr(1, 2)
   >>> repr(x)
   'UseEasyRepr(foo=1, bar=2)'

"Angle" Style
-------------

The other built-in style is "angle" style, defined by
:func:`easyrepr.style.angle_style`, which formats the repr similar to
:func:`object.__repr__`. To set this style, pass ``style="<>"`` (a string of
less-than sign and greater-than sign).

.. code-block:: pycon
   :caption: Repr using "angle" style

   >>> from easyrepr import easyrepr
   ...
   >>> class UseEasyRepr:
   ...     def __init__(self, foo, bar):
   ...         self.foo = foo
   ...         self.bar = bar
   ...
   ...     @easyrepr(style="<>")
   ...     def __repr__(self):
   ...         ...
   ...
   >>> x = UseEasyRepr(1, 2)
   >>> repr(x)
   '<UseEasyRepr foo=1 bar=2>'

User-Defined Style
------------------

You may also pass a user-defined style function. The function should accept
three parameters: the object instance, the computed class name, and an iterable
of attribute descriptions (tuples of length one or two).

When implementing a style function, the :func:`easyrepr.style.format_attribute`
utility function is useful to format the attribute description tuples.

.. code-block:: pycon
   :caption: Repr with a user-defined style function

   >>> from easyrepr import easyrepr, style
   ...
   >>> def my_style(obj, class_name, attributes):
   ...     formatted_attributes = ", ".join(
   ...         map(style.format_attribute, attributes)
   ...     )
   ...     obj_id = id(obj)
   ...     return (
   ...         f"{class_name}"
   ...         f" with id {obj_id}"
   ...         f" and attributes {formatted_attributes}"
   ...     )
   ...
   >>> class UseEasyRepr:
   ...     def __init__(self, foo, bar):
   ...         self.foo = foo
   ...         self.bar = bar
   ...
   ...     @easyrepr(style=my_style)
   ...     def __repr__(self):
   ...         ...
   ...
   >>> x = UseEasyRepr(1, 2)
   >>> repr(x)  # doctest: +ELLIPSIS
   'UseEasyRepr with id ... and attributes foo=1, bar=2'


Inheritance
===========

Easyrepr plays nicely with inheritance. In general, classes inherit the
configuration of their ancestors, to which they can append new attributes.

Simple Inheritance
------------------

If an ancestor class uses easyrepr, the ancestor's attributes will be included
first.

.. code-block:: pycon
   :caption: Repr with simple inheritance

   >>> from easyrepr import easyrepr
   ...
   >>> class BaseEasyRepr:
   ...     def __init__(self, foo, bar):
   ...         self.foo = foo
   ...         self.bar = bar
   ...
   ...     @easyrepr
   ...     def __repr__(self):
   ...         return ('foo', 'bar')
   ...
   >>> class DerivedEasyRepr(BaseEasyRepr):
   ...     def __init__(self, foo, bar, baz):
   ...         super().__init__(foo, bar)
   ...         self.baz = baz
   ...
   ...     @easyrepr
   ...     def __repr__(self):
   ...         return ('baz',)
   ...
   >>> x = DerivedEasyRepr(1, 2, 3)
   >>> repr(x)
   'DerivedEasyRepr(foo=1, bar=2, baz=3)'

Multiple Inheritance
--------------------

If a class has multiple ancestor classes that use easyrepr, their attributes
will be included in *reverse* MRO (method resolution order) --- i.e., attributes
of ancestor classes later in the MRO will be included earlier.

.. code-block:: pycon
   :caption: Repr with multiple inheritance

   >>> from easyrepr import easyrepr
   ...
   >>> class BaseEasyRepr:
   ...     def __init__(self, foo, bar):
   ...         self.foo = foo
   ...         self.bar = bar
   ...
   ...     @easyrepr
   ...     def __repr__(self):
   ...         return ('foo', 'bar')
   ...
   >>> class MixinEasyRepr:
   ...     def __init__(self, *args, a, b, c, **kwargs):
   ...         super().__init__(*args, **kwargs)
   ...         self.a = a
   ...         self.b = b
   ...         self.c = c
   ...
   ...     @easyrepr
   ...     def __repr__(self):
   ...         return ('a', 'b', 'c')
   ...
   >>> class DerivedEasyRepr(MixinEasyRepr, BaseEasyRepr):
   ...     def __init__(self, foo, bar, baz, **kwargs):
   ...         super().__init__(foo, bar, **kwargs)
   ...         self.baz = baz
   ...
   ...     @easyrepr
   ...     def __repr__(self):
   ...         return ('baz',)
   ...
   >>> x = DerivedEasyRepr(1, 2, 3, a=4, b=5, c=6)
   >>> repr(x)
   'DerivedEasyRepr(foo=1, bar=2, a=4, b=5, c=6, baz=3)'

Inheriting Style
----------------

If a class does not set an explicit style, and an ancestor class does, the
closest ancestor class's style (in MRO order) will be used. (If no ancestor sets
an explicit style, :ref:`the default will be used<"Call" Style>` as usual.)

.. code-block:: pycon
   :caption: Repr with inherited style

   >>> from easyrepr import easyrepr
   ...
   >>> class BaseEasyRepr:
   ...     def __init__(self, foo, bar):
   ...         self.foo = foo
   ...         self.bar = bar
   ...
   ...     @easyrepr(style='<>')
   ...     def __repr__(self):
   ...         return ('foo', 'bar')
   ...
   >>> class DerivedEasyRepr(BaseEasyRepr):
   ...     def __init__(self, foo, bar, baz):
   ...         super().__init__(foo, bar)
   ...         self.baz = baz
   ...
   ...     @easyrepr
   ...     def __repr__(self):
   ...         return ('baz',)
   ...
   >>> x = DerivedEasyRepr(1, 2, 3)
   >>> repr(x)
   '<DerivedEasyRepr foo=1 bar=2 baz=3>'

Inheritance with Ellipsis
-------------------------

If an ancestor class has an easyrepr :obj:`__repr__` method that uses
:obj:`None` or :obj:`Ellipsis` (also spelled :any:`...`) to include all public
attributes, that repr will include all attributes of the *object*, including
those added by derived classes.

This is not really a feature of inheritance --- *any* public attribute of the
object, regardless of its source, would be included --- but it comes up most
frequently with inheritance.

.. code-block:: pycon
   :caption: Repr with simple inheritance

   >>> from easyrepr import easyrepr
   ...
   >>> class BaseEasyRepr:
   ...     def __init__(self, foo, bar):
   ...         self.foo = foo
   ...         self.bar = bar
   ...
   ...     @easyrepr
   ...     def __repr__(self):
   ...         ...
   ...
   >>> class DerivedEasyRepr(BaseEasyRepr):
   ...     def __init__(self, foo, bar, baz):
   ...         super().__init__(foo, bar)
   ...         self.baz = baz
   ...
   >>> x = DerivedEasyRepr(1, 2, 3)
   >>> repr(x)
   'DerivedEasyRepr(foo=1, bar=2, baz=3)'

Overriding Inherited Methods
----------------------------

A class can override the usual search for ancestor :obj:`__repr__` methods by
passing ``override=True`` to :func:`~easyrepr.easyrepr`.

.. note::

  Even with ``override=True``, :obj:`__repr__` may still refer to attributes set
  by ancestor classes (even private ones, if desired) since attributes are not
  actually associated to a class.

.. code-block:: pycon
   :caption: Repr overriding inherited method

   >>> from easyrepr import easyrepr
   ...
   >>> class BaseEasyRepr:
   ...     def __init__(self, foo, bar):
   ...         self.foo = foo
   ...         self.bar = bar
   ...
   ...     @easyrepr(style='<>')
   ...     def __repr__(self):
   ...         return ('foo', 'bar')
   ...
   >>> class DerivedEasyRepr(BaseEasyRepr):
   ...     def __init__(self, foo, bar, baz):
   ...         super().__init__(foo, bar)
   ...         self.baz = baz
   ...
   ...     @easyrepr(override=True)
   ...     def __repr__(self):
   ...         return ('baz',)
   ...
   >>> x = DerivedEasyRepr(1, 2, 3)
   >>> repr(x)
   'DerivedEasyRepr(baz=3)'
