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

   $ pip install easyrepr

.. _available on PyPI: https://pypi.org/project/easyrepr/

From Source
-----------

For development, you can check out the source `from GitHub`_ and create a
virtual environment using |poetry-link|_.

.. code-block:: console

   $ git clone https://github.com/chrisbouchard/easyrepr.git
   $ cd easyrepr
   $ poetry install

.. _from GitHub: https://github.com/chrisbouchard/easyrepr
.. |poetry-link| replace:: ``poetry``
.. _poetry-link: https://python-poetry.org/


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

If an item in the sequence is a :obj:`tuple` like ``(name, value)`` (i.e., with
two elements), easyrepr will interpret it as a "virtual attribute", which lets
you provide a name and value directly. The virtual attribute does *not* have to
correspond to an actual attribute of the object.

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

If an item in the sequence is a :obj:`tuple` like ``(value,)`` (i.e., with one
element), easyrepr will interpret it as a *nameless* virtual attribute. The
value will be included in the generated repr directly.

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
