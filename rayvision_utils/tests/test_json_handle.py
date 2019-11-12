"""Test rayvision_utils.json_handle model."""

# Import third-party modules
# pylint: disable=import-error
import pytest

from rayvision_utils.exception.exception import VersionNotMatchError


def test_valid(json_handle):
    """Test save_tips this interface.

    Test We can get an ``VersionNotMatchError`` if the information is wrong.

    """
    json_handle.name = ''
    json_handle.version = '2505'
    with pytest.raises(VersionNotMatchError):
        json_handle.valid()


@pytest.mark.parametrize('location, exe_name, data', [
    (None, 'maya.exe', None),
    ('/nas/txt', 'mayabatch.exe', None),
    ('c:/abc/maya2018', 'maya.exe', None),
    (None, 'render.exe', None),
])
def test_exe_path_from_location(json_handle, location, exe_name, data):
    """Test we can get None."""
    result = json_handle.exe_path_from_location(location, exe_name)
    assert result == data


def test_json_exist(json_handle):
    """Test json_exist this function, we can get correct result."""
    result = json_handle.json_exist()
    assert result[0] is False
    assert 'Json file is not generated' in result[1]
