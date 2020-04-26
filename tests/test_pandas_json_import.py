from datetime import datetime

import numpy as np
import pandas as pd
import pytest
from pandas.util.testing import assert_frame_equal

from notebooks.pandas.pandas_json_import import expand


@pytest.fixture
def base_dict():
    return {'int': 42, 'string': 'answer', 'float': 3.14, 'object': datetime(2020, 1, 1)}


@pytest.fixture
def base_list():
    return [10, 20, 30]


@pytest.fixture
def complex_dict(base_dict):
    d = {
        'list_of_dict': [base_dict.copy(), base_dict.copy(), {}],
        'nested_dict': {'a': {'b': {
            'x': 1, 'y': 2, 'z': [100, 200, {'c': 300}]
        }}},
    }
    return d


def make_dataframe(data, n: int = 3):
    """Create a list of dicts with length n and convert it into a data frame."""
    return pd.DataFrame([data] * n)


def test_expand_empty_dataframe():
    result = expand(pd.DataFrame())

    expected = pd.DataFrame()

    assert_frame_equal(result, expected)


def test_expand_basic_dataframe(base_dict):
    result = expand(make_dataframe(base_dict))

    expected = make_dataframe(base_dict)

    assert_frame_equal(result, expected)


def test_expand_empty_dict(base_dict):
    test_dict = base_dict.copy()
    test_dict['dict'] = {}
    result = expand(make_dataframe(test_dict))

    expected = make_dataframe(base_dict)  # columns with empty dicts are removed

    assert_frame_equal(result.sort_index(axis=1), expected.sort_index(axis=1))


def test_expand_one_item_dict(base_dict):
    test_dict = base_dict.copy()
    test_dict['dict'] = {'int': 42}
    result = expand(make_dataframe(test_dict))

    expected = pd.concat([
        make_dataframe(base_dict),
        make_dataframe({'dict_int': 42})
    ], axis=1)

    assert_frame_equal(result.sort_index(axis=1), expected.sort_index(axis=1))


def test_expand_dict(base_dict):
    test_dict = base_dict.copy()
    test_dict['dict'] = base_dict.copy()
    result = expand(make_dataframe(test_dict))

    expected = pd.concat([
        make_dataframe(base_dict),
        make_dataframe(
            {'dict_int': 42, 'dict_string': 'answer', 'dict_float': 3.14, 'dict_object': datetime(2020, 1, 1)}
        )
    ], axis=1)

    assert_frame_equal(result.sort_index(axis=1), expected.sort_index(axis=1))


def test_expand_empty_list(base_dict):
    test_dict = base_dict.copy()
    test_dict['list'] = []
    result = expand(make_dataframe(test_dict))

    expected = make_dataframe(base_dict)  # columns with empty lists are removed

    assert_frame_equal(result.sort_index(axis=1), expected.sort_index(axis=1))


def test_expand_one_item_list(base_dict, base_list):
    test_dict = base_dict.copy()
    test_dict['list'] = [10]
    result = expand(make_dataframe(test_dict))

    expected = pd.concat([
        make_dataframe(base_dict),
        make_dataframe({'list_0': 10})
    ], axis=1)

    assert_frame_equal(result.sort_index(axis=1), expected.sort_index(axis=1))


def test_expand_list(base_dict, base_list):
    test_dict = base_dict.copy()
    test_dict['list'] = base_list
    result = expand(make_dataframe(test_dict))

    expected = pd.concat([
        make_dataframe(base_dict),
        make_dataframe({'list_0': 10, 'list_1': 20, 'list_2': 30})
    ], axis=1)

    assert_frame_equal(result.sort_index(axis=1), expected.sort_index(axis=1))


def test_expand_dicts_of_different_length(base_dict):
    n = 3
    data = [base_dict.copy() for __ in range(n)]
    data[0]['dict'] = {}
    data[1]['dict'] = {'int': 42}
    data[2]['dict'] = base_dict.copy()
    result = expand(pd.DataFrame(data))

    expected = pd.concat([
        pd.DataFrame([base_dict] * n),
        pd.DataFrame([
            {'dict_int': np.nan, 'dict_string': np.nan, 'dict_float': np.nan, 'dict_object': np.nan},
            {'dict_int': 42, 'dict_string': np.nan, 'dict_float': np.nan, 'dict_object': np.nan},
            {'dict_int': 42, 'dict_string': 'answer', 'dict_float': 3.14, 'dict_object': datetime(2020, 1, 1)},
        ])
    ], axis=1)

    assert_frame_equal(result.sort_index(axis=1), expected.sort_index(axis=1))


def test_expand_lists_of_different_length(base_dict, base_list):
    n = 3
    data = [base_dict.copy() for __ in range(n)]
    data[0]['list'] = []
    data[1]['list'] = [10]
    data[2]['list'] = base_list
    result = expand(pd.DataFrame(data))

    expected = pd.concat([
        pd.DataFrame([base_dict] * n),
        pd.DataFrame([
            {'list_0': np.nan, 'list_1': np.nan, 'list_2': np.nan},
            {'list_0': 10, 'list_1': np.nan, 'list_2': np.nan},
            {'list_0': 10, 'list_1': 20, 'list_2': 30},
        ])
    ], axis=1)

    assert_frame_equal(result.sort_index(axis=1), expected.sort_index(axis=1))


def test_expand_complex_dict(complex_dict):
    result = expand(make_dataframe(complex_dict))

    expected = make_dataframe({
        'list_of_dict_0_int': 42,
        'list_of_dict_0_string': 'answer',
        'list_of_dict_0_float': 3.14,
        'list_of_dict_0_object': datetime(2020, 1, 1),
        'list_of_dict_1_int': 42,
        'list_of_dict_1_string': 'answer',
        'list_of_dict_1_float': 3.14,
        'list_of_dict_1_object': datetime(2020, 1, 1),
        'nested_dict_a_b_x': 1,
        'nested_dict_a_b_y': 2,
        'nested_dict_a_b_z_0': 100,
        'nested_dict_a_b_z_1': 200,
        'nested_dict_a_b_z_2_c': 300,
    })

    assert_frame_equal(result.sort_index(axis=1), expected.sort_index(axis=1))


def test_custom_columns(complex_dict):
    result = expand(make_dataframe(complex_dict),
                    custom_columns={'list_of_dict': lambda x: x, 'nested_dict': lambda x: str(x)})

    expected = make_dataframe(complex_dict)
    expected['nested_dict'] = expected['nested_dict'].apply(str)

    assert_frame_equal(result, expected)


def test_expand_recursive_dict(base_dict):
    base_dict['dict'] = base_dict  # infinite nesting

    with pytest.raises(RuntimeError):
        expand(make_dataframe(base_dict), depth=5)
