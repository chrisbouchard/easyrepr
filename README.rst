========
easyrepr
========

.. image:: https://badge.fury.io/py/easyrepr.svg
   :alt: PyPI
   :target: https://pypi.org/project/easyrepr/
.. image:: https://circleci.com/gh/chrisbouchard/easyrepr/tree/main.svg?style=shield
   :alt: CircleCI
   :target: https://circleci.com/gh/chrisbouchard/easyrepr/tree/main
.. image:: https://readthedocs.org/projects/easyrepr/badge/
   :alt: Read the Docs
   :target: https://easyrepr.readthedocs.io/en/latest/
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

Python decorator to automatically generate repr strings

Example
=======

.. code-block:: pycon

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

Installation
============

.. code-block:: console

   $ pip install easyrepr