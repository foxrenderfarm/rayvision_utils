"""Test rayvision_utils.analyze_handle model."""

# Import third-party modules
# pylint: disable=import-error
import pytest

from rayvision_utils.analyse_handle import RayvisionAnalyse
from rayvision_utils.exception.exception import RayvisionError


def test_rayvision_analyze(task):
    """Test RayvisionAnalyse this class.

    Test We can get an ``RayvisionError`` if the class is wrong.

    """
    with pytest.raises(RayvisionError):
        RayvisionAnalyse(task)
