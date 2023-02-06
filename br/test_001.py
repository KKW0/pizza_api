import gazu

gazu.client.set_host("http://192.168.3.116/api")
gazu.set_event_host("http://192.168.3.116")
gazu.log_in("pipeline@rapa.org", "netflixacademy")

project_name = "Test_bbr"

gazu.files.update_project_file_tree(Test_bbr,
                                    dict(working=dict(mountpoint="/working_files", root="productions", folder_path={
                                        "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>",
                                        "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>",
                                        "sequence": "<Project>/sequences/<Sequence>>/<TaskType>",
                                        "style": "lowercase"
                                    }, file_name={
                                        "shot": "<Project>_<Sequence>_<Shot>_<TaskType>",
                                        "asset": "<Project>_<AssetType>_<Asset>_<TaskType>",
                                        "sequence": "<Project>_<Sequence>_<TaskType>",
                                        "style": "lowercase"
                                    }), output={
                                        "mountpoint": "/output_files",
                                        "root": "productions",
                                        "folder_path": {
                                            "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>",
                                            "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>",
                                            "sequence": "<Project>/sequences/<Sequence>>/<TaskType>",
                                            "style": "lowercase"
                                        },
                                        "file_name": {
                                            "asset": "<Project>_<AssetType>_<Asset>_<TaskType>",
                                            "shot": "<Project>_<Sequence>_<Shot>_<TaskType>",
                                            "sequence": "<Project>_<Sequence>_<TaskType>",
                                            "style": "lowercase"
                                        }
                                    }, preview={
                                        "mountpoint": "/preview_files",
                                        "root": "productions",
                                        "folder_path": {
                                            "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>",
                                            "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>",
                                            "sequence": "<Project>/sequences/<Sequence>>/<TaskType>",
                                            "style": "lowercase"
                                        },
                                        "file_name": {
                                            "asset": "<Project>_<AssetType>_<Asset>_<TaskType>",
                                            "shot": "<Project>_<Sequence>_<Shot>_<TaskType>",
                                            "sequence": "<Project>_<Sequence>_<TaskType>",
                                            "style": "lowercase"
                                        }
                                    }))

working = gazu.files.new_working_file
# task =


output = gazu.files.build_entity_output_file_path
# entity =
# output_type =
# task_type =



