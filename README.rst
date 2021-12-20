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

Easyrepr is `available on PyPI`_, so the easiest method of installation is via
``pip``.

.. code-block:: console

   $ pip install easyrepr

For more installation options, see the `Installation section in the User Guide`_.

.. _available on PyPI: https://pypi.org/project/easyrepr/
.. _Installation section in the User Guide:
   https://easyrepr.readthedocs.io/en/latest/guide.html#installation


Documentation
=============

For full documentation, check out `easyrepr on Read the Docs`_.

* `User Guide`_
* `API Reference`_

.. _easyrepr on Read the Docs: https://easyrepr.readthedocs.io/en/latest/
.. _User Guide: https://easyrepr.readthedocs.io/en/latest/guide.html
.. _API Reference: https://easyrepr.readthedocs.io/en/latest/api.html


Contributing
============

If you're interesting in contributing to easyrepr, or just want to learn more
about how the project is built or structured, please read our `CONTRIBUTING
file`_.

.. _CONTRIBUTING file: CONTRIBUTING.rst


License
=======

The `MIT license`_ applies to all files in the easyrepr repository and source
distribution. See the `LICENSE file`_ for more info.

.. _MIT license: https://choosealicense.com/licenses/mit/
.. _LICENSE file: LICENSE.rst
