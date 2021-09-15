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
a repr based on :func:`vars`.

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
