========
easyrepr
========

Welcome to the documentation for easyrepr, a Python decorator to automatically
generate repr strings.

Example
=======

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

Contents
========

.. toctree::

   guide
   api
   license
