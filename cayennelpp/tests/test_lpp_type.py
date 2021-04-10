import pytest

from cayennelpp.lpp_type import LppType


def test_init_invalid_type():
    with pytest.raises(Exception):
        LppType("foo", "bar", [1], [1], [False])


def test_init_invalid_name():
    with pytest.raises(Exception):
        LppType("foo", "bar", [1], [1], [False])


def test_init_invalid_sizes():
    with pytest.raises(Exception):
        LppType("foo", "bar", [1, 1], [1], [False])


def test_init_invalid_scales():
    with pytest.raises(Exception):
        LppType("foo", "bar", [1], [1, 1], [False])


def test_init_invalid_signs():
    with pytest.raises(Exception):
        LppType("foo", "bar", [1], [1], [False, False])


def test_get_lpp_type_invalid():
    with pytest.raises(Exception):
        LppType.get_lpp_type("foo")


def test_get_lpp_type_none():
    assert not LppType.get_lpp_type(42)
