import gazu

class FileTree:

    def __init__(self, project):
        self.project = project
        self.file_tree = project.get("file_tree")
        self._mountpoint = None
        self._root = None

    @property
    def mnt_point(self):
        return self._mountpoint

    @mnt_point.setter
    def mnt_point(self, value):
        self._mountpoint = value

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    def init_file_tree(self):
        if not self.file_tree:
            return self.update_filetree()
        elif


    def update_filetree(self):
        tree = {
            "working": {
                "mountpoint": self._mountpoint,
                "root": self._root,
                "folder_path": {
                    "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/working/v<Revision>",
                    "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/working/v<Revision>",
                    "style": "lowercase"
                },
                "file_name": {
                    "shot": "<Project>_<Sequence>_<Shot>_<TaskType>_<Revision>",
                    "asset": "<Project>_<AssetType>_<Asset>_<TaskType>_<Revision>",
                    "style": "lowercase"
                }
            },
            "output": {
                "mountpoint": self._mountpoint,
                "root": self._root,
                "folder_path": {
                    "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/output/<OutputType>/v<Revision>",
                    "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/output/<OutputType>/v<Revision>",
                    "style": "lowercase"
                },
                "file_name": {
                    "shot": "<Project>_<Sequence>_<Shot>_<OutputType>_v<Revision>",
                    "asset": "<Project>_<AssetType>_<Asset>_<OutputType>_v<Revision>",
                    "style": "lowercase"
                }
            }
        }
        gazu.files.update_project_file_tree(self.project, tree)

