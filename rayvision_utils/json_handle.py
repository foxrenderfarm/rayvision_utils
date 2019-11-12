"""CG base model.

Mainly to process some configuration information of CG software, and write it
into json file.

"""

# Import built-in modules
from __future__ import division
from __future__ import print_function

import logging
import os
import traceback

# Import local modules
from rayvision_utils import utils
from rayvision_utils.cmd import Cmd
from rayvision_utils.exception import tips_code
from rayvision_utils.exception.error_msg import VERSION_NOT_MATCH
from rayvision_utils.exception.exception import VersionNotMatchError
from rayvision_utils.exception.tips import TipsInfo


# pylint: disable=useless-object-inheritance
class JsonHandle(object):
    """CG basic module."""

    def __init__(self, cg_file, task, cg_id, custom_exe_path):
        """Initialize the configuration of the CG software."""
        self.name = None
        self.exe_path = None
        self.version = None
        self.version_str = None
        self.local_os = utils.get_os()  # windows/linux.
        self.cg_file = cg_file
        self.task = task
        self.cg_id = cg_id
        self.custom_exe_path = custom_exe_path

        self.task_json = None
        self.asset_json = None
        self.tips_json = None
        self.upload_json = None
        self.cmd = Cmd()
        self.tips = TipsInfo(save_path=task.work_dir)

        # handle `user_input`.
        user_id = self.task.task_info["task_info"]["user_id"]
        user_parent_id = int(user_id) // 500 * 500
        self.user_input = "{0}/{1}".format(user_parent_id, user_id)

        self.logger = logging.getLogger(__name__)

    def __repr__(self):
        """Output all instance variables of the object.

        Returns:
            str: Instance variable information.
                e.g.:
                    "tips=<rayvision_core.utils.CG.tips.TipsInfo object at
                        0x04210B70>".
                    "user_input=100093000/100093088".
                    "log=<Logger analyse (DEBUG)>".

        """
        return "\n".join(['{0}={1}'.format(k, v) for k, v in
                          self.__dict__.items()])

    def valid(self):
        """Check CG software.

        Check if there is a problem with the configuration. If there is a
        problem, it will be written in the tips.

        Raises:
            VersionNotMatchError: The version of the CG software does not
                match.

        """
        self.logger.debug("[Rayvision_utils base valid start .....]")
        software_config = self.task.task_info["software_config"]
        cg_version = software_config["cg_version"]
        cg_name = software_config["cg_name"]
        if ((cg_name.capitalize() != self.name.capitalize())
                or (cg_version != self.version)):
            self.tips.add(tips_code.CG_NOTMATCH, self.version_str)
            self.tips.save_tips()
            raise VersionNotMatchError(VERSION_NOT_MATCH)
        self.logger.debug("[Rayvision_utils base valid end .....]")

    def dump_task_json(self):
        """Write the basic information of the scene to the file."""
        self.logger.debug("[Rayvision_utils base dump_task_json start .....")
        task_json = self.task.task_info
        utils.json_save(self.task.task_json_path, task_json,
                        ensure_ascii=False)
        self.logger.debug("[Rayvision_utils base dump_task_json end .....")

    def run(self):
        """Throw an exception directly.

        Raises:
            NotImplementedError: You should override this method.

        """
        raise NotImplementedError("You should override this method")

    def exe_path_from_location(self, location, exe_name):
        """Check if the startup file of the CG software exists.

        Returns:
            str or None: There is a return path, there is no return to None.

        """
        exe_path = None
        if location is not None:
            exe_path = os.path.join(location, exe_name)
            if not os.path.exists(exe_path):
                self.logger.debug(exe_path)
                return None
        return exe_path

    def load_output_json(self):
        """Load the output path and information.

        Read the data in task.json, asset.json.tips.json, and update the data
        corresponding to the task.

        """
        self.task_json = self.json_load(self.task.task_json_path)
        self.asset_json = self.json_load(self.task.asset_json_path)
        self.tips_json = self.json_load(self.task.tips_json_path)

        self.task.task_info = self.task_json
        self.task.asset_info = self.asset_json
        self.task.tips_info = self.tips_json

    def json_load(self, json_path, encodings=None):
        """Get the data of the json file in the path by the specified encoding.

        Args:
            json_path (str): Json file path.
            encodings (list): Encoding list, default is None.
                e.g.:
                    ["utf-8", "gbk"]

        Returns:
            dict: Data in the json file.

        Raises:
            FileExistsError: Json file path does not exist.
            Exception: Other exception.

        """
        if encodings is None:
            encodings = ["utf-8"]
        dict_data = {}
        for index, encoding in enumerate(encodings):
            try:
                dict_data = utils.json_load(json_path, encoding=encoding)
                break
            except (IOError, UnicodeError):
                if index == len(encodings) - 1:
                    self.logger.error("error load: %s\n%s", json_path,
                                      traceback.format_exc())
                continue
        return dict_data

    def write_cg_path(self):
        """Update data in task.json.

        Process the path of the scene file and the CG software id and write it
        to the task.json file.

        """
        self.task.task_info["task_info"]["input_cg_file"] = (
            self.cg_file.replace("\\", "/"))
        self.task.task_info["task_info"]["cg_id"] = self.cg_id

        utils.json_save(self.task.task_json_path, self.task.task_info,
                        ensure_ascii=False)

    def json_exist(self):
        """Check if the task's task.json, asset.json, tips.json path exists.

        Returns:
            tuple: Whether the path exists and prompt information.
                e.g.:
                    (False, "Json file is not generated c:/tips.json").

        """
        for json_path in [self.task.task_json_path, self.task.asset_json_path,
                          self.task.tips_json_path]:
            if not os.path.exists(json_path):
                msg = "Json file is not generated: {0}".format(json_path)
                return False, msg
        return True, None
