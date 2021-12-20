========================
Contributing to Easyrepr
========================

Welcome to the easyrepr project! We welcome contributions. Please read on to
learn about how the project is developed, and how you can contribute.

One thing to keep in mind: this project is a hobby for me. All work on the
project will be best-effort in my spare time, with no promises on the timeline.


Important Resources
===================

* `Project page on GitHub`_
* `Project page on PyPI`_
* `Documentation on Read the Docs`_
* `CI Pipeline on CircleCI`_

.. _Project page on GitHub: https://github.com/chrisbouchard/easyrepr
.. _Project page on PyPI: https://pypi.org/project/easyrepr/
.. _Documentation on Read the Docs: https://easyrepr.readthedocs.io
.. _CI Pipeline on CircleCI: https://circleci.com/gh/chrisbouchard/easyrepr


Contributing
============

The preferred path to contributing is to open an issue in the GitHub project
describing your error, use-case, idea, etc. While I do try to create issues to
document all my own plans and ideas for the project, it's possible your change
is one I'm already working on, or possibly one that I will soon render
unnceessary by a different change.

After creating an issue, you're welcome to follow up with a pull request. I'll
review your pull request as soon as I have time. If you are not comfortable
making the change yourself, and I think the change is a good one, I would be
happy to do it myself as time allows.

All changes must include unit tests to cover the new functionality or fix, as
well as new or updated documentation as appropriate. All pull requests must pass
the CI (continuous integration) pipeline on CircleCI to be merged into the
``main`` branch.


Developing
==========

Easyrepr is a Python library written in Python. The project is defined by
`pyproject.toml`_ using `Poetry`_. Once you've `installed Poetry`_, you can
check out and install the project for development.

.. code-block:: console

   $ git clone https://github.com/chrisbouchard/easyrepr.git
   $ cd easyrepr
   $ poetry install

Poetry will automatically create a virtual environment for the project and
install the required dependencies. After installing the project, you can use
Poetry to start a shell inside the virtual environment.

.. code-block:: console

   $ poetry shell

You can also use Poetry to run a single command inside the virtual environment.

.. code-block:: console

   $ poetry run pytest

Checkout `Poetry's documentation`_ for a more thorough explanation of what you
can do.

.. _pyproject.toml: pyproject.toml
.. _Poetry: https://python-poetry.org
.. _installed Poetry: https://python-poetry.org/docs/
.. _Poetry's documentation: https://python-poetry.org/docs/basic-usage/


Code Structure
--------------

The easyrepr library itself lives in the ``easyrepr`` directory. It comprises a
few submodules:

``easyrepr.decorator``
  The definition of the ``@easyrepr`` decorator. This is the main entrypoint
  into the library for users.

``easyrepr.descriptor``
  The definition of the ``EasyRepr`` descriptor, and the core component of the
  library. ``EasyRepr`` is not directly exported, but used through the
  ``@easyrepr`` directive.

``easyrepr.reflection``
  Internal utilities around inspecting objects for their attributes.

``easyrepr.style``
  Style function definitions to format repr strings.


.. _section Code Standards:

Code Standards
--------------

Easyrepr uses `Black`_ as its code formatter. All code merged into ``main`` must
pass Black's check as part of CI. Many editors let you integrate Black so that
your Python code is automatically reformatted when you save.

We also run the `flake8`_ linter. Code merged into ``main`` must have no linter
errors. Preferrably, this is due to fixing the code to pass the linter, but if
necessary this could be by adding a comment to ignore a particular error on a
line that triggers an insane lint error. All linter comments *must* be preceded
by a comment explaining why it's necessary to ignore this particular error in
this particular location.

.. _Black: https://black.readthedocs.io
.. _flake8: https://flake8.pycqa.org


.. _section Testing:

Testing
-------

Easyrepr uses `PyTest`_ to run unit tests. All functionality *should* be covered
by a unit test, though we do not currently measure coverage.

You can run tests inside your Poetry virtual environment:

.. code-block:: console

   $ poetry run pytest

The projects PyTest configuration will run all tests detected in the ``tests``
directory, as well as doctests for all ``pycon`` code blocks in the
documentation. Note: We don't consider the doctests for test coverage; their
purpose is to help ensure that our documentation stays correct as the code
evolves.

All new features or bug fixes must be covered by new unit tests.

.. _PyTest: https://docs.pytest.org


.. _section Typing:

Typing
------

We do not currently require type annotations in easyrepr. However, we do run
`MyPy`_ in our build pipeline as a sanity check.

.. _MyPy: http://mypy-lang.org


.. _section Documenting:

Documenting
-----------

The documentation for easyrepr lives in ``docs``. We use `Sphinx`_ to build the
documentation from the `reStructuredText`_ files in that directory.

To build the documentation locally, use the ``Makefile`` in the ``docs``
directory. This requires you have a ``make`` tool installed.

.. code-block:: console

   $ poetry run make html

Note that you'll need to run ``make`` inside the Poetry virtual environment.

All new features should include a new section in the documentation explaining its
use, and an example ``pycon`` code block demonstrating it. The example code
blocks are automatically tested by PyTest so that we can keep the documentation
up-to-date as the project evolves.

.. _Sphinx: https://www.sphinx-doc.org
.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html


Build Processes
===============

Pull requests and merges into ``main`` trigger continuous integration processes.
All CI checks must pass in order to merge a pull request into ``main``. These
are managed via integrations between GitHub and the various other services.


.. _section CircleCI:

CircleCI
--------

The workflow in `CircleCI`_ will run `unit tests`_, `lints`_, and `static
analysis`_ on each branch. It also attempts to build a wheel. The workflow is
defined in ``.circleci/config.yml``.

.. _CircleCI: https://circleci.com
.. _unit tests: `section Testing`_
.. _lints: `section Code Standards`_
.. _static analysis: `section Typing`_


Read the Docs
-------------

`Read the Docs`_ watches the project and rebuilds the `documentation`_ for each
pull request and for ``main``.

.. _Read the Docs: https://readthedocs.org
.. _documentation: `section Documenting`_


Tagged Releases
---------------

Releases of easyrepr are managed via tags, which are automatically detected by
the workflow in Circle CI when they are pushed to ``main``. Release tags have
the format ``vX.Y.Z``, where *X.Y.Z* (e.g., 1.2.3) is the version triple for the
new release.

Pushing a tag with this format to ``main`` will cause CircleCI to automatically
publish the wheel to PyPI at the end of the `workflow`_.

.. _workflow: `section CircleCI`_
