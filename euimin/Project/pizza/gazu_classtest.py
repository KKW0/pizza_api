import gazu
import os
import pprint as pp

class CRUD:
    def __int__(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.set_event_host("http://192.168.3.116")
        gazu.log_in("pipeline@rapa.org", "nextflixacademy")
        self._asset_name = None
        self._asset_info = {}
        self._task_type = None
        self._extension = None
        self._path = os.getcwd()


    @property
    def asset_name(self):
        return self._asset_name

    @asset_name.setter
    def asset_name(self, asset_value):
        self._asset_name = asset_value

    @property
    def task_type(self):
        return self._task_type

    @task_type.setter
    def task_type(self, task_value):



def main():
    crud = CRUD()
    crud.asset_name = 'Hulkbuster'
    crud.task_type = 'Modeling'
    crud.extension = 'png'
