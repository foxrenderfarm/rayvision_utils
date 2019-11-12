"""analyze.

Check the scene file and CG startup file, select the analysis script of CG
software.

"""

# Import built-in modules
import os

# Import local modules
from rayvision_utils.exception.exception import RayvisionError


# pylint: disable=useless-object-inheritance
class RayvisionAnalyse(object):
    """Analyze which CG process to follow."""

    def __init__(self, task, exe_path=None):
        """Initialize the basic information of the rendering.

        Generate the object of the cmd command that builds the startup
        analysis script

        Args:
            task (rayvision_api.tasks.core.RayvisionTask): Task object.
            exe_path (str, optional): Users can manually specify the exe path
                of the cg software. If there is any way to use this path
                directly, it will not be automatically found.

        """
        self.cg_id = task.task_info['task_info']['cg_id']
        self.cg_file = task.task_info['task_info']['input_cg_file']
        self.task = task
        self.custom_exe_path = exe_path
        self.cg_instance = self.create_instance()

    def create_instance(self):
        """Create a startup analysis script object.

        Check scene files and startup files of custom CG software, generate
        the object of the cmd command that builds the startup analysis script.

        Returns:
            object: Construct the object of the cmd command that starts the
                analysis script.
                e.g.:
                    Maya.

            Raises:
                RayvisionError: The scene file does not exist. The file path
                    of the startup CG software is incomplete or not a file.

        """
        if not os.path.isfile(self.cg_file):
            raise RayvisionError(1000000,
                                 "Cg file does not exist: {0}".
                                 format(self.cg_file))

        if self.custom_exe_path is not None:
            if not os.path.isabs(self.custom_exe_path):
                raise RayvisionError(1000000,
                                     "Please specify the exe full path")
            if not os.path.isfile(self.custom_exe_path):
                raise RayvisionError(1000000,
                                     "The specified exe path does not exist")

        cg_id = self.cg_id
        param_dict = {
            'cg_id': self.cg_id,
            'cg_file': self.cg_file,
            'task': self.task,
            'custom_exe_path': self.custom_exe_path
        }

        if cg_id == '2000':
            # pylint: disable=import-error
            from rayvision_maya.analyze_maya_handle import Maya
            cg_instance = Maya(**param_dict)
        elif cg_id == '2004':
            # pylint: disable=import-error
            from rayvision_houdini.cg import Houdini
            cg_instance = Houdini(**param_dict)
        elif cg_id == '2013':
            # pylint: disable=import-error
            from rayvision_clarisse.analyse_clarisse import Clarisse
            cg_instance = Clarisse(**param_dict)
        else:
            raise RayvisionError(1000000, "The cg_id does not exist!")

        return cg_instance

    @classmethod
    def execute(cls, task, exe_path=None):
        """Start analysis.

        Create a cmd command to start the analysis script and Start the entire
        analysis process.

        Args:
            task (RayvisionTask): Task object.
            exe_path (str, optional): Users can manually specify the exe path
                of the cg software. If there is any way to use this path
                directly, it will not be automatically found.

        """
        self = cls(task, exe_path)
        self.run()
        scene_info_data = self.task.task_info['scene_info']

        self.task.task_info['scene_info_render'] = scene_info_data
        self.cg_is_maya(self.cg_id, task.task_info['scene_info'])

    @staticmethod
    def cg_is_maya(cg_id, scene_info_data):
        """Execute when CG software is Maya.

        Set the details of the frames that need to be rendered for each layer.

        Args:
            cg_id (str): CG software id.
            scene_info_data (dict): Analyzed scene information
                e.g.:
                    {
                        "defaultRenderLayer": {
                            "renderable": "1",
                            "is_default_camera": "1",
                            "common": {
                                "renderer": "mayaSoftware",
                                "image_file_prefix": "",
                                "start": "1",
                                "end": "10",
                                "by_frame": "1",
                                "frames": "1-10[1]",
                                "all_camera": [
                                  "perspShape"
                                ],
                                "render_camera": [
                                  "perspShape"
                                ],
                                "renumber_frames": "False",
                                "width": "960",
                                "height": "540",
                                "image_format": "iff",
                                "animation": "True"
                            },
                              "option": "",
                              "env": {}
                        }
                        "layer1": {
                            "renderable": "1",
                            "is_default_camera": "1",
                            "common": {
                                "renderer": "mayaSoftware",
                                "image_file_prefix": "",
                                "start": "",
                                "end": "",
                                "by_frame": "",
                                "frames": "",
                                "all_camera": [
                                  "perspShape"
                                ],
                                "render_camera": [
                                  "perspShape"
                                ],
                                "renumber_frames": "False",
                                "width": "960",
                                "height": "540",
                                "image_format": "iff",
                                "animation": "True"
                            },
                              "option": "",
                              "env": {}
                        }
                    }

        Returns:
            dict: Set the scene information of the frame details to be
            rendered for each layer.

        """
        if cg_id == '2000':  # Maya.
            for layer_name, layer_dict in scene_info_data.items():
                start_frame = layer_dict['common']['start']
                end_frame = layer_dict['common']['end']
                by_frame = layer_dict['common']['by_frame']
                frames = '{0}-{1}[{2}]'.format(start_frame,
                                               end_frame, by_frame)
                scene_info_data[layer_name]['common']['frames'] = frames

        return scene_info_data

    def run(self):
        """Start the entire analysis process."""
        self.cg_instance.run()

    def analyse_cg_file(self):
        """Analyze CG software information for making scene files."""
        self.cg_instance.analyse_cg_file()

    def analyse(self):
        """Analysis scene information in CG software."""
        self.cg_instance.analyse()
