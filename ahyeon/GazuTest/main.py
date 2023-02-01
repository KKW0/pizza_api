import os
import gazu
import pprint as pp


class GetSelectedPreviews:
    """
    테스크 타입을 선택하고, 해당하는 obj 프리뷰 파일들만 저장하는 클래스
    """
    def __init__(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.set_event_host("http://192.168.3.116")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")
        self._asset_name = ""
        self._task_type = ''
        self._extension = ''
        self._asset_info = {}
        self._path = os.getcwd()

    @property
    def asset_name(self):
        return self._asset_name

    @asset_name.setter
    def asset_name(self, value):
        self._asset_name = value

    @property
    def task_type(self):
        return self._task_type

    @task_type.setter
    def task_type(self, value):
        self._task_type = value

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, value):
        self._extension = value

    def get_asset_info(self):
        """
        원하는 에셋 정보를 받아오는 함수
        """
        project = gazu.project.get_project_by_name("NetflixAcademy")
        self._asset_info = gazu.asset.get_asset_by_name(project, self.asset_name)
        print("\n### asset info ###")
        pp.pprint(self._asset_info)

    def get_task_type(self):
        """
        에셋에 있는 모든 테스크 타입들 중 원하는 테스크 타입을 받아오는 함수
        """
        self.get_asset_info()
        task_type_list = gazu.task.all_task_types_for_asset(self._asset_info['id'])
        print("\n### all task type info ###")
        pp.pprint(task_type_list)
        for item in task_type_list:
            if item['name'] == self.task_type:
                return item

    def get_task_info(self):
        """
        에셋에서 선택한 테스크 타입의 테스크 정보를 받아오는 함수
        """
        task_type = self.get_task_type()
        selected_task = gazu.task.get_task_by_name(self._asset_info, task_type['id'])
        print("\n### selected task info ###")
        pp.pprint(selected_task)

        return selected_task

    def get_previews_info(self):
        """
        에셋의 선택된 테스크에 속한 프리뷰 파일들의 인포

        """
        selected_task = self.get_task_info()
        previews = gazu.files.get_all_preview_files_for_task(selected_task['id'])
        print("\n### all preview files ###")
        pp.pprint(previews)

        return previews

    def download_previews(self):
        """
        원하는 타입의 프리뷰 파일을 저장하는 함수
        """
        previews = self.get_previews_info()
        num = 0
        for preview_item in previews:
            if preview_item['extension'] == self.extension:
                gazu.files.download_preview_file(preview_item['id'],
                                                 self._path+"/hulk"+str(num)
                                                 +"."+self.extension)
                num += 1

    def get_main_preview(self):
        """
        대표 프리뷰 파일 하나의 정보를 받고 저장하는 함수
        저장 경로는 현재 py 파일이 실행되는 폴더
        """
        preview_dict = gazu.files.get_preview_file(self._asset_info['preview_file_id'])
        print("\n### main preview file info ###")
        pp.pprint(preview_dict)
        gazu.files.download_preview_file(preview_dict['id'],
                                         self._path+"/hulk."+preview_dict['extension'])


def main():
    obj = GetSelectedPreviews()
    obj.task_type = 'Modeling'
    obj.extension = 'png'
    obj.asset_name = 'Hulkbuster'
    obj.download_previews()


if __name__ == "__main__":
    main()
