# -*- coding:utf-8 -*-
"""Test rayvision_utils.utils functions."""

# Import third-party modules
# pylint: disable=import-error
import pytest

# Import local models
from rayvision_utils.utils import check_contain_chinese
from rayvision_utils.utils import convert_path
from rayvision_utils.utils import get_os
from rayvision_utils.utils import json_load
from rayvision_utils.utils import json_save
from rayvision_utils.utils import str2unicode


@pytest.mark.parametrize('test_case, results', [
    ('D:/work/render/19183793/max/d/Work/c05/112132P-embery.jpg',
     '/D/work/render/19183793/max/d/Work/c05/112132P-embery.jpg'),
    ('//pipeline/test/path', '/pipeline/test/path')
])
def test_convert_path(test_case, results):
    """Test convert_path this interface."""
    assert convert_path(test_case) == results


def test_json_load(tmpdir):
    """Test the json_load feature.

    Test We can get an ``IOError`` if the information is wrong.

    """
    _path = tmpdir.mkdir("test_examples1")
    json_path = _path.join("tests.json")
    with pytest.raises(IOError):
        json_load(str(json_path))

    json_path_chines = _path.join("天天.json")
    with pytest.raises(IOError):
        json_load(str(json_path_chines))


@pytest.mark.parametrize("data, encoding", [
    ({"a": 123}, 'utf-8'),
])
def test_json_save(data, encoding, tmpdir):
    """Test the json_save feature.

    Test We can get an ``IOError`` if the information is wrong.

    """
    _path = tmpdir.mkdir("test_examples2")
    json_path = _path.mkdir("small")
    with pytest.raises(IOError):
        json_save(str(json_path), data, encoding)

    json_path_chinese = _path.mkdir("小")
    with pytest.raises(IOError):
        json_save(str(json_path_chinese), data, encoding)


@pytest.mark.parametrize("string", ['sneck', '蛇'])
def test_check_contain_chinese(string):
    """Test the check_contain_chinese feature.

    Test We can get an bool.

    """
    result = check_contain_chinese(string)
    assert isinstance(result, bool)


def test_get_os():
    """Test the get_os feature.

    Test We can get an string.

    """
    result = get_os()
    assert isinstance(result, str)


@pytest.mark.parametrize("handle_str, str_decode", [
    ('rayvision', 'default'),
    ('瑞云', 'utf-8'),
    ('技术', 'gbk'),
    ('sdk', 'gbk')
])
def test_str2unicode(handle_str, str_decode):
    """Test the str2unicode feature.

    Test We can get an string.

    """
    result = str2unicode(handle_str, str_decode)
    assert isinstance(result, str)
