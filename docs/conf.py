import easyrepr
import importlib.metadata
import inspect
import logging
import os
import pathlib
import subprocess
import sys


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# -- Project information -----------------------------------------------------

easyrepr_dist = importlib.metadata.distribution("easyrepr")

project = easyrepr_dist.metadata["Name"]
author = easyrepr_dist.metadata["Author"]
copyright = f"2021 {author} & Contributors"

# The full version, including alpha/beta/rc tags
release = easyrepr_dist.version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

html_theme_options = {
    "github_user": "chrisbouchard",
    "github_repo": "easyrepr",
    "extra_nav_links": {
        "GitHub": "https://github.com/chrisbouchard/easyrepr",
        "Issues": "https://github.com/chrisbouchard/easyrepr/issues",
        "PyPI": "https://pypi.org/project/easyrepr/",
    },
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Extension configuration -------------------------------------------------

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}


try:
    linkcode_url_format = os.environ["LINKCODE_URL_FORMAT"]
    # Read the Docs sometimes adds unnecessary quotes to environment variables.
    # Until readthedocs/readthedocs.org#8636 is resolved, we need to strip them
    # manually to be safe.
    linkcode_url_format = linkcode_url_format.strip("'")
except KeyError:
    logger.exception(
        "Environment variable LINKCODE_URL_FORMAT is not set, disabling linkcode."
    )
    extensions.remove("sphinx.ext.linkcode")

# Get git commit and GitHub URL for linkcode
try:
    git_hash = subprocess.run(
        "git rev-parse --short HEAD",
        capture_output=True,
        shell=True,
        check=True,
        text=True,
    ).stdout.strip()
except subprocess.SubprocessError:
    logger.exception("Cannot get git commit, disabling linkcode.")
    extensions.remove("sphinx.ext.linkcode")

# Get the parent directory of the easyrepr module. We'll resolve files against
# this directory.
# E.g., if easyrepr's source file is /foo/bar/easyrepr/__init__.py, we'll
# resolve against /foo/bar.
easyrepr_dir = pathlib.Path(inspect.getsourcefile(easyrepr)).parent.parent.resolve()


def find_source(module, fullname):
    obj = sys.modules[module]
    for part in fullname.split("."):
        obj = getattr(obj, part)

    source_file = pathlib.Path(inspect.getsourcefile(obj)).resolve()
    filename = source_file.relative_to(easyrepr_dir)

    source, start_line = inspect.getsourcelines(obj)
    end_line = start_line + len(source) - 1

    return filename, start_line, end_line


# Resolve function for the linkcode extension.
def linkcode_resolve(domain, info):
    module = info["module"]
    fullname = info["fullname"]

    if domain != "py" or not module:
        return None

    filename, start_line, end_line = find_source(module, fullname)

    return linkcode_url_format.format(
        git_hash=git_hash,
        filename=filename,
        start_line=start_line,
        end_line=end_line,
    )
