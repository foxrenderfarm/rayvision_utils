"""Test rayvision_utils.exception.exception model."""

# Import third-party modules
# pylint: disable=import-error
import pytest

from rayvision_utils.exception.exception import RayvisionAPIError
from rayvision_utils.exception.exception import RayvisionError


def test_rayvison_error():
    """Test rayvison error this interface."""
    def post_info():
        raise RayvisionError(20000, 'Rayvision Error.')

    with pytest.raises(RayvisionError) as err:
        post_info()
        assert err.error_code == 20000
        assert err.error == 'Rayvision Error.'


def test_rayvision_api_error():
    """Test rayvison api error this interface."""
    def post_info():
        raise RayvisionAPIError(123415, 'Rayvision Error.', 'tests.com')

    with pytest.raises(RayvisionError) as err:
        post_info()
        assert err.error_code == 123415
