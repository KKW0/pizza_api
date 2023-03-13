# coding:utf8

import gazu
import pprint as pp
import tkinter as tk



# from login import LogIn

"""
Kitsu에 로그인한 상태에서 task entity(레이아웃 에셋)의 메인 프리뷰 url을 구하고,
구한 url에서부터 데이터를 받아오는 모듈
"""

gazu.client.set_host("http://192.168.3.116/api")
gazu.log_in("pipeline@rapa.org", "netflixacademy")


class ThumbNail(tk):

    def __init__(self, parent):
        self.info_frame = None
        tk.__init__(self, parent)

    def _get_thumbnail(self, preview):
        """
        Kitsu에서 썸네일 데이터를 받아오는 매서드

        Args:
            preview(dict): main preview의 딕셔너리

        Returns:
            data(png): main preview의 사진
        """
        url = gazu.files.get_preview_file_url(preview)
        data = gazu.client.get_file_data_from_url(url)

        return data

    def canvas_click(self, event):
        # 작업이 선택되었는지 확인
        if self.selected_task:
            # 360도 카메라 표시
            self.display_camera()

        else:
            # 캐스팅 썸네일 및 정보 표시
            self.display_castings()

    def display_camera(self):
        # 360도 카메라 표시 코드
        pass

    def display_castings(self):
        # 데이터베이스에서 선택한 에 가져오기
        asset_id = self.get_selected_asset_id()
        # 선택한 에셋에 대한 캐스팅 가져오기
        castings = gazu.casting.get_asset_casting(asset_id)
        # 각 캐스팅에 대한 미리 보기 및 정보 목록 만들기
        casting_info = []

        for casting in castings:
            thumbnail = self.get_casting_thumbnail(casting)
            name = self.get_casting_name(casting)
            description = self.get_casting_description(casting)
            casting_info.append({'thumbnail': thumbnail, 'name': name, 'description': description})

    def get_casting_thumbnail(self, casting):
        # 데이터베이스에서 캐스팅 섬네일을 가져오는 코드
        pass

    def get_casting_name(self, casting):
        # 데이터베이스에서 이름을 가져오는 코드
        pass

    def get_casting_description(self, casting):
        # 데이터베이스에서 설명을 가져오는 코드
        pass

    def thumbnail_control(self, task_list_or_dict, task_num=None, casting_info_list=None, undi_info_list=None):
        """

        Args:
            task_list_or_dict(list/dict): 사용자가 선택한 테스크, 또는 필터링한 테스크 딕셔너리의 집합
                                          task_num의 타입이 int면 딕셔너리, None이면 리스트 타입이다.
            task_num(int): 사용자가 선택한 테스크의 인덱스 번호. 사용자가 task를 선택하기 전에는 None
            casting_info_list(list): 사용자가 task를 선택하기 전에는 None
                                    [asset_name, description, asset_type_name, nb_occurences]
            undi_info_list(list): 사용자가 task를 선택하기 전에는 None
                                 [output file name, output type name, comment, description, entity_id]

        Returns:
            png: 메인 썸네일의 png
            list: 캐스팅된 에셋들의 썸네일 png의 집합
            png: 언디스토션 이미지의 썸네일
        """

        if task_num is None:
            # 테스크 선택 전에는 첫번째 테스크의 메인 썸네일을 return 한다.
            layout_asset = gazu.entity.get_entity(task_list_or_dict[0]['entity_id'])
            preview = gazu.files.get_preview_file(layout_asset['preview_file_id'])
            png = self._get_thumbnail(preview)

            return png
        else:
            # 테스크 선택 시 선택한 테스크의 메인 썸네일과 캐스팅 목록의 썸네일들을 return 한다.
            asset_thumbnail_list = []
            undi_png = None
            layout_asset = gazu.entity.get_entity(task_list_or_dict['entity_id'])
            preview = gazu.files.get_preview_file(layout_asset['preview_file_id'])
            png = self._get_thumbnail(preview)

            for info in casting_info_list:
                # 캐스팅된 에셋들의 썸네일 및 정보 표시
                proj = gazu.project.get_project(task_list_or_dict[task_num]['project_id'])
                asset = gazu.asset.get_asset_by_name(proj, info[0])
                preview = gazu.files.get_preview_file(asset['preview_file_id'])
                asset_thumbnail_list.append(self._get_thumbnail(preview))

                thumbnail = tk.Label(self.info_frame, image=info['thumbnail'])
                thumbnail.pack()
                name_label = tk.Label(self.info_frame, text=info['name'])
                name_label.pack()
                description_label = tk.Label(self.info_frame, text=info['description'])
                description_label.pack()

            for info in undi_info_list:
                # 언디스토션 이미지의 썸네일
                shot = gazu.shot.get_shot(info['entity_id'])
                preview = gazu.files.get_preview_file(shot['preview_file_id'])
                undi_png = self._get_thumbnail(preview)

            return png, asset_thumbnail_list, undi_png

            # 카메라는 썸네일 없음

def main():
    root = tk()
    root.mainloop()
    aa = ThumbNail()
    aa.thumbnail_control



if __name__ == "__main__":
    main()
