import pytest

from cayennelpp.lpp_type import LppType


def test_init_invalid_type():
    with pytest.raises(TypeError):
        LppType("foobar", "foobar", [1], [1], [False])


def test_init_invalid_name():
    with pytest.raises(TypeError):
        LppType(42, 42, [1], [1], [False])


def test_init_invalid_sizes():
    with pytest.raises(TypeError):
        LppType(42, "foobar", 42, [1], [False])


def test_init_invalid_scales():
    with pytest.raises(TypeError):
        LppType(42, "foobar", [1], 42, [False])


def test_init_invalid_signs():
    with pytest.raises(TypeError):
        LppType(42, "foobar", [1], [1], 42)


def test_init_invalid_sizes_len():
    with pytest.raises(ValueError):
        LppType(42, "foobar", [1, 1], [1], [False])


def test_get_lpp_type_invalid():
    with pytest.raises(TypeError):
        LppType.get_lpp_type("foo")


def test_get_lpp_type_none():
    assert not LppType.get_lpp_type(999)
