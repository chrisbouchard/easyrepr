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

   The ``skip_private`` argument only affects how :obj:`None` and
   :obj:`Ellipsis` are handled. Attribute names specified as strings are always
   included.

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
