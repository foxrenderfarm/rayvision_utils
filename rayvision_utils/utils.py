"""The CG util functions."""

# Import built-in models
from __future__ import unicode_literals

from builtins import str
import codecs
import json
import logging
import platform
import re
import sys


# Python version.
VERSION = sys.version_info[0]


def json_load(json_path, encoding='utf-8'):
    """Load the data from the json file.

    Args:
        json_path (str): Json file path.
        encoding (str): Encoding, default is ``utf-8``.

    Returns:
        dict: Data in the json file.
            e.g.:
                {
                    "task_info"
                }

    """
    with codecs.open(json_path, 'r', encoding=encoding) as f_json:
        data = json.load(f_json)

    return data


def json_save(json_path, data, encoding='utf-8', ensure_ascii=True):
    """Will save to the json file according to the specified encoded data.

    Args:
        json_path (str): Json file path.
        data (dict): Asset information data.
            e.g.:
                {
                    "scene_info": {
                        "defaultRenderLayer":{
                            "renderable": "1",
                            "is_default_camera": "1",
                        }
                    }
                }
        encoding (str): Encoding, default is ``utf-8``.
        ensure_ascii (bool): Whether to ignore the error, default ``True``.

    """
    with codecs.open(json_path, 'w', encoding=encoding) as f_json:
        if VERSION == 3:
            json.dump(data, f_json, ensure_ascii=ensure_ascii, indent=2)
        else:
            f_json.write(str(json.dumps(data, ensure_ascii=ensure_ascii,
                                        indent=2)))


def convert_path(path):
    """Convert to the path the server will accept.

    Args:
        path (str): Local file path.
            e.g.:
                "D:/work/render/19183793/max/d/Work/c05/112132P-embery.jpg"

    Returns:
        str: Path to the server.
            e.g.:
                "/D/work/render/19183793/max/d/Work/c05/112132P-embery.jpg"

    """
    lower_path = path.replace('\\', '/')
    if lower_path[1] == ":":
        path_lower = lower_path.replace(":", "")
        path_server = "/" + path_lower
    else:
        path_server = lower_path[1:]

    return path_server


def check_contain_chinese(string):
    """Check if string has Chinese.

    Args:
        string (str): String to be checked.

    Returns:
        bool: True means there is, False means no.

    """
    pattern = re.compile('[\u4e00-\u9fa5]+')
    match = pattern.search(string)
    if match:
        return True
    return False


def str2unicode(handle_str, str_decode='default'):
    """Decode the string.

    Args:
        handle_str (str or bytes): String to be decoded.
        str_decode (str): What encoding needs to be decoded, the default
            is lowercase.

    Returns:
        str: Need to decode the string.

    """
    if not isinstance(handle_str, str):
        try:
            if str_decode != 'default':
                handle_str = handle_str.decode(str_decode.lower())
            else:
                try:
                    handle_str = handle_str.decode('utf-8')
                except (AttributeError, UnicodeError):
                    try:
                        handle_str = handle_str.decode('gbk')
                    except (AttributeError, UnicodeError):
                        handle_str = handle_str.decode(
                            sys.getfilesystemencoding())
        except (AttributeError, UnicodeError) as err_message:
            logger = logging.getLogger(__name__)
            logger.warning('str2unicode: `%s` decode failed', handle_str)
            logger.warning(str(err_message))
    return handle_str


def get_os():
    """Get system name.

    Returns:
        str: The system/OS name.
            e.g.:
                ``Linux`` or ``Windows``.

    """
    return platform.system().lower()
