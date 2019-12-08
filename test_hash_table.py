from unittest.mock import MagicMock, call
from . import HashTable
import pytest


@pytest.fixture()
def empty_hash_table():
    return HashTable()


@pytest.fixture()
def filled_hash_table():
    return HashTable([1, 2, 3])


def test_init():
    seed = [1, 2, 3]
    # substitution of method add for MagicMock
    original_add = HashTable.add
    HashTable.add = MagicMock()
    # calling of __init__ with argument seed which indicates method add
    HashTable(seed)
    # Checking if add method was called for every element
    HashTable.add.assert_has_calls([
        call(value) for value in seed
    ])
    HashTable.add = original_add


def test_init_empty_seed():
    original_add = HashTable.add
    HashTable.add = MagicMock()
    HashTable(seed=[])
    HashTable.add.assert_not_called()
    HashTable.add = original_add


def test_add(empty_hash_table):
    # given
    value = 3
    # when
    empty_hash_table.add(value)
    # then
    values_list = list(empty_hash_table)
    assert len(values_list) == 1
    assert value in values_list


def test_remove(filled_hash_table):
    # given
    value = 2
    # when
    filled_hash_table.remove(value)
    # then
    values_list = list(filled_hash_table)
    assert len(values_list) == 2
    assert value not in values_list


def test_remove_not_exists(filled_hash_table):
    # given
    value = 5
    # when & then
    with pytest.raises(ValueError):
        filled_hash_table.remove(value)


def test_contains(filled_hash_table):
    # given
    value = 1
    # when
    result = value in filled_hash_table
    # then
    assert result is True


def test_not_contains(filled_hash_table):
    # given
    value = 5
    # when
    result = value in filled_hash_table
    # then
    assert result is False


def test_add_unique_items(empty_hash_table):
    # given
    value = 2
    # when
    empty_hash_table.add(value)
    empty_hash_table.add(value)
    # then
    values_list = list(empty_hash_table)
    assert len(values_list) == 1
    assert value in values_list


def test_resize(empty_hash_table):
    values = [ 0, 1,     3,  4, 5,    7,
               8, 9, 10, 11, 12,
               16, 17, 18
            ]
    hash_table = HashTable()
    for value in values:
        empty_hash_table.add(value)
    assert len(empty_hash_table) / empty_hash_table.size < empty_hash_table.FILL_RATIO


def test_dynamic_initial_size():
    pass
