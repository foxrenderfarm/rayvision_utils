"""Handle tips messages and write them to tips.json."""

# Import built-in modules
import os
import sys

# Import local modules
from rayvision_utils import utils
from rayvision_utils.exception.exception import RayvisionError


# pylint: disable=useless-object-inheritance
class TipsInfo(object):
    """Handling errors encountered in the analysis."""

    def __init__(self, save_path=None):
        """Initialize the tips.json path and tips message.

        Args:
            save_path (str): The configuration information path path.

        """
        self.tips_list = {}
        self.path = save_path

    def add(self, key, *values):
        """Add tips message.

        Args:
            key (str): TipsInfo code.
            values (tuple): TipsInfo message.
                e.g.:
                    ('Scene file no exists', 'Missing renderer')

        """
        if key in self.tips_list:
            for value in values:
                self.tips_list[key].append(value)
        else:
            self.tips_list[key] = list(values)

    def set_tips(self, key, value):
        """Set tips message.

        Args:
            key (str): TipsInfo code.
            value (str): TipsInfo message.

        """
        self.tips_list[key] = value

    def save_tips(self, path=None):
        """Save the prompt to the tips.json file.

        Args:
            path (str, optional): The configuration information path path.

        """
        if path is None:
            if self.path:
                path = self.path
            else:
                raise RayvisionError(20003,
                                     "The TipsInfo' path is not defined.")

        filename = os.path.join(path, "tips.json")
        utils.json_save(filename, self.tips_list, ensure_ascii=False)

    def save_and_exit(self, path, exit_code=-1):
        """Save the prompt to the tips.json file and exit.

        Args:
            path (str): The configuration information path path.
            exit_code (int): Exit code, default is -1.

        """
        self.save_tips(path)
        sys.exit(exit_code)
