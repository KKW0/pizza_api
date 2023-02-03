import gazu
import pprint as pp

class UpdateKitsu:

    def __init__(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.set_event_host("http://192.168.3.116")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")
        self._project = ""
        self._asset_type = ""
        self._asset = ""
        self._seq = ""
        self._shot = ""
        self._task_type = ""

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, value):
        self._project = gazu.project.get_project_by_name(value)

    @property
    def asset_type(self):
        return self._asset_type

    @asset_type.setter
    def asset_type(self,value):
        self._asset_type = value

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, value):
        self._asset = value

    @property
    def seq(self):
        return self._seq

    @seq.setter
    def seq(self, value):
        self._seq = gazu.shot.get_sequence_by_name(self.project, value)

    @property
    def shot(self):
        return  self._shot

    @shot.setter
    def shot(self, value):
        self._shot = gazu.shot.get_shot_by_name(self.seq, value)

    @property
    def task_type(self):
        return self._task_type

    @task_type.setter
    def task_type(self, value):
        self.task_type = value

    def get_project_info(self):
        project = gazu.project.get_project_by_name(self._project)
        return project

    def new_asset_type(self):
        asset_type = gazu.asset.new_asset_type(self._asset_type)
        return asset_type

    def new_seq(self):
        sequence = gazu.shot.new_sequence(self.get_project_info(), self._seq, episode=None,)
        return sequence

    def new_shot(self):
        shot = gazu.shot.new_shot(self._project,self.new_seq(), self._shot)
        return shot

    def get_tesk_type(self):
        task_type = gazu.new_task_type_2(self._task_type, entity)
        return task_type

    def new_task(self):
        task = gazu.task.new_task(self.new_shot(), self.get_tesk_type())
        return task

    def set_list_data(self, data):
        input_list = data.split()
        output_list = []
        num = 1
        for x in input_list:
            if x not in output_list:
                output_list.append(x)
            else:
                sum = x + '%s' % num
                output_list.append(sum)
                num += 1

        return output_list

    def set_asset_task_kitsu(self):
        asset_type_list = self.set_list_data(self._asset_type)
        asset_list = self.set_list_data(self._asset)
        task_type_list = self.set_list_data(self._task_type)
        for asset_type in asset_type_list:
            asset_types = gazu.asset.new_asset_type(asset_type)


def main():
    tree = {
      "working": {
        "mountpoint": "/mnt/project/pizza",
        "root": "pizza",
        "folder_path": {
          "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>",
          "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>",
          "sequence": "<Project>/sequences/<Sequence>>/<TaskType>",
          "style": "lowercase"
        },
        "file_name": {
          "shot": "<Project>_<Sequence>_<Shot>_<TaskType>",
          "asset": "<Project>_<AssetType>_<Asset>_<TaskType>",
          "sequence": "<Project>_<Sequence>_<TaskType>",
          "style": "lowercase"
        }
      }
    }

    gz = UpdateKitsu()
    gz.project = 'PIZZA'
    gz.seq = 'jeongtae'
    gz.shot = 'jeongtae01'
    print(gz.shot)



if __name__ == "__main__":
    main()