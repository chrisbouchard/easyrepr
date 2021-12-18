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


Documentation
=============

For full documentation, check out `easyrepr on Read the Docs`_.

* `User Guide`_
* `API Reference`_

.. _easyrepr on Read the Docs: https://easyrepr.readthedocs.io/en/latest/
.. _User Guide: https://easyrepr.readthedocs.io/en/latest/guide.html
.. _API Reference: https://easyrepr.readthedocs.io/en/latest/api.html


License
=======

MIT License

Copyright © 2021 Chris Bouchard & Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
