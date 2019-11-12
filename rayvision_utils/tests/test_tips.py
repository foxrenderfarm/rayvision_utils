"""Test rayvision_utils.exception.tips model."""

import os

# Import third-party modules
# pylint: disable=import-error
import pytest


def test_save_tips(tips, tmpdir):
    """Test save_tips this interface. we can find tips.json"""
    tips.save_tips(str(tmpdir))
    assert os.path.exists(str(tmpdir.join('tips.json'))) is True


@pytest.mark.parametrize('key, value', [
    ('test1', 'car1'),
    (123, 'car@#$2'),
    ('te.st3', 'c,./ar3'),
    ('tes0.t4', 'ca8769(r4'),
])
def test_set_tips(tips, key, value):
    """Test save_tips this interface.

    Test We can get an ``RayvisionError`` if the information is wrong.

    """
    tips.set_tips(key, value)
    assert tips.tips_list[key] == value
