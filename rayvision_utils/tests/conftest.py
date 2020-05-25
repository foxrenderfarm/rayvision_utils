"""The plugin of the pytest.

The pytest plugin hooks do not need to be imported into any test code, it will
load automatically when running pytest.

References:
    https://docs.pytest.org/en/2.7.3/plugins.html

"""

# pylint: disable=import-error
import pytest

from rayvision_utils.cmd import Cmd


@pytest.fixture()
def user_info():
    """Get user info."""
    return {
        "domain": "task.renderbus.com",
        "platform": "2",
        "access_id": "df6d1d6s3dc56ds6",
        "access_key": "fa5sd565as2fd65",
        "local_os": 'windows',
        "workspace": "c:/workspace",
        "render_software": "Maya",
        "software_version": "2018",
        "project_name": "Project1",
        "plugin_config": {
            "mtoa": "3.1.2.1"
        }
    }


@pytest.fixture()
def cg_file(tmpdir):
    """Get render config."""
    return {
        'cg_file': str(tmpdir.join('muti_layer_test.ma'))
    }


@pytest.fixture()
def handle_cmd():
    """Get a Cmd object."""
    return Cmd()


@pytest.fixture()
def api(user_info):
    from rayvision_api import RayvisionAPI
    render_para = {
        "domain": user_info["domain"],
        "platform": user_info["platform"],
        "access_id": user_info["access_id"],
        "access_key": user_info["access_key"],
    }
    return RayvisionAPI(**render_para)


@pytest.fixture()
def check(api):
    """Create an RayvisionCheck object."""
    from rayvision_api.task.check import RayvisionCheck
    return RayvisionCheck(api)


@pytest.fixture()
def upload_info():
    """Get upload info."""
    return {
        "scene": [
            {
                "local": "D:\\ziyuan\\class01\\feichuan.project",
                "server": "/D/ziyuan/class01/feichuan.project"
            }
        ],
        "asset": [
            {
                "local": "D:\\ziyuan\\class01\\T\\anli\\NO.2_class\\"
                         "mp48319259_1450060453032_1_th.jpeg",
                "server": "/D/ziyuan/class01/T/anli/NO.2_class/"
                          "mp48319259_1450060453032_1_th.jpeg"
            },
        ]
    }


@pytest.fixture()
def tips():
    """Create an TipsInfo object."""
    from rayvision_utils.exception.tips import TipsInfo
    return TipsInfo()
