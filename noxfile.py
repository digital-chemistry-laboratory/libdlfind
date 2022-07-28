"""Automated testing linting and formatting apparatus."""

import nox
from nox.sessions import Session

package = "libdlfind"
nox.options.sessions = "lint", "tests", "mypy"  # default session
locations = "libdlfind", "test", "noxfile.py"  # Linting locations
pyversions = ["3.8", "3.9", "3.10"]


# Testing
@nox.session(python=pyversions)
def tests(session: Session) -> None:
    """Run tests."""
    args = session.posargs + ["--cov=libdlfind", "--import-mode=importlib", "-s"]
    session.install("-r", "requirements-test.txt")
    session.install(".")
    session.run("pytest", *args)


# Linting
@nox.session(python="3.9")
def lint(session: Session) -> None:
    """Lint code."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
        "flake8-annotations",
        "flake8-docstrings",
        "darglint",
    )
    session.run("flake8", *args)


# Code formatting
@nox.session(python="3.9")
def black(session: Session) -> None:
    """Format code."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


# Static typing
@nox.session(python="3.9")
def mypy(session: Session) -> None:
    """Run the static type checker."""
    args = session.posargs or locations
    session.install("mypy")
    session.install("types-pkg_resources")
    session.run("mypy", *args)
