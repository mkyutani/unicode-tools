"""Basic tests for unicode_tools package."""

import pytest
from unicode_tools import uchr


def test_package_import():
    """Test that the package can be imported."""
    import unicode_tools
    assert unicode_tools is not None


def test_uchr_module_import():
    """Test that the uchr module can be imported."""
    from unicode_tools import uchr
    assert uchr is not None


def test_uchr_function_exists():
    """Test that the main uchr function exists."""
    from unicode_tools.uchr import uchr
    assert callable(uchr) 