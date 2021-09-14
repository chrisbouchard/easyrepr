easyrepr
========

Welcome to the documentation for easyrepr, a Python decorator to automatically
generate repr strings.

Example
-------

.. doctest::

   >>> class UseEasyRepr:
   ...     def __init__(self, foo, bar):
   ...         self.foo = foo
   ...         self.bar = bar
   ...     @easyrepr
   ...     def __repr__(self):
   ...         ...
   ...
   >>> x = UseEasyRepr(1, 2)
   >>> repr(x)
   'UseEasyRepr(foo=1, bar=2)'

Installation
------------

::

    $ pip install easyrepr

API Reference
-------------

.. toctree::

   api
