# -*- coding=utf-8 -*-
"""Test cmd.py."""

import pytest


@pytest.mark.parametrize('cmd_str, result', [
    ('gogogo', 'gogogo'),
    ('名', '名'),
    ('renderbus', 'renderbus'),
])
def test_compatible(handle_cmd, cmd_str, result):
    """Test compatible, we can get a expected result."""
    cmd = handle_cmd.compatible(cmd_str)
    assert cmd == result
