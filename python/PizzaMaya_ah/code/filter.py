#coding:utf8
import pprint

import gazu
import pprint as pp
from thumbnail import thumbnail_control


class Filter:
    def __init__(self):
        # gazu.client.set_host("http://192.168.3.116/api")
        # gazu.log_in("keiel0326@gmail.com", "tmvpdltm")
        pass

    def _get_information_dict(self, task):
        """
        각 task에서 필터링에 필요한 정보들을 추출하여 딕셔너리에 추가하는 매서드

        Args:
            task(dict): 유저에게 할당된 task

        Returns:
            dict(task_info): task에서 필요한 정보만 추출하여 모은 딕셔너리
            str(seq['name']: task asset이 속한 시퀀스의 이름
        """
        task_info = dict()
        task_info['project_name'] = task['project_name']
        task_info['due_date'] = task['due_date']
        task_info['description'] = task['description']
        task_info['last_comment'] = task['last_comment']
        # task asset이 사용되는 seq 구하기
        task_asset = gazu.asset.get_asset(task['entity_id'])
        casted_list = gazu.casting.get_asset_cast_in(task_asset)
        seq = dict
        for cast in casted_list:
            if cast['shot_name'] is not None:
                shot = gazu.shot.get_shot(cast['shot_id'])
                seq = gazu.shot.get_sequence_from_shot(shot)
                task_info['sequence_name'] = seq['name']
                return task_info, seq['name']
            else:
                continue

    def _collect_info_task(self):
        """
        필터링에 필요한 프로젝트 이름, 시퀀스 이름을 proj_set, seq_set에 중복 없이 모으고,
        각 task의 정보를 모아 반환하는 매서드

        Returns:
            list(task_info_list): task의 정보들 중 사용자에게 노출할 정보들만 모은 딕셔너리의 집합
            list(task_list): 사용자에게 assign되었고, task status가 _Todo 또는 WIP인  모든 task 딕셔너리의 집합
            list(proj_set): 각 task가 속한 프로젝트의 이름들을 중복없이 모든 리스트
            list(seq_set): 각 task asset이 사용되는 시퀀스의 이름들을 중복없이 모은 리스트
        """
        seq_list = []
        proj_list = []
        task_info_list = []
        task_list = gazu.user.all_tasks_to_do()
        for task in task_list:
            proj_list.append(task['project_name'])
            task_info, seq_name = self._get_information_dict(task)
            task_info_list.append(task_info)
            seq_list.append(seq_name)
        proj_set = list(set(proj_list))
        seq_set = list(set(seq_list))

        return task_info_list, task_list, proj_set, seq_set

    def _list_append(self, shot, output_type):
        """
        리스트에 아웃풋 파일(언디스토션 이미지, camera)의 정보를 담는다

        Args:
            shot(dict): 언디스토션 이미지, 카메라의 아웃풋 파일이 속한 shot
            output_type(dict): 아웃풋 파일이 속한 아웃풋 타입

        Returns:
            list: output file의 모델에서 필요한 정보들만 담은 리스트의 집합
        """
        info_list = []
        task_type = gazu.task.get_task_type_by_name('Matchmove')
        output_list = gazu.files.get_last_output_files_for_entity(shot, output_type, task_type)
        for output in output_list:
            if output is None:
                raise ValueError("해당하는 output file이 존재하지 않습니다.")
            else:
                info_list.append([output['name'], output_type['name'], output['comment'], output['description'],
                                  output['entity_id']])
                return info_list

    def _collect_info_casting(self, task):
        """
        선택한 task가 속한 asset(task asset)에 casting된 에셋들의 정보 중 필요한 내용을 추출하여 저장한다.
        task asset이 캐스팅된 샷의 언디스토션 이미지와 camera output의 정보 중 필요한 내용을 추출한다.

        Args:
            task(dict): 선택한 task의 딕셔너리

        Returns:
            list(casting_info_list): 캐스팅된 에셋들의 정보를 담은 리스트의 집합
                                     (asset name, description, asset type name, nb_occurences)
            list(undi_info_list): task asset에 캐스팅된 샷의 언디스토션 이미지 정보를 담은 리스트의 집합
                                 (output type name, comment, description)
            list(camera_info_list): task asset에 캐스팅된 샷의 카메라 정보를 담은 리스트의 집합
                                    (output type name, comment, description)
        """
        self._get_information_dict(task)
        casting_info_dict = []
        undi_info_list = []
        camera_info_list = []
        task_asset = gazu.asset.get_asset(task['entity_id'])
        all_casting_list = gazu.casting.get_asset_casting(task_asset)
        for cast in all_casting_list:
            asset = gazu.asset.get_asset(cast['asset_id'])
            casting_dict = {'asset_name': cast['asset_name'],
                            'description': asset['description'],
                            'asset_type_name': cast['asset_type_name'],
                            'nb_occurences': cast['nb_occurences'],
                            'revision': cast['revision'],
                            'comment': cast['comment']}
            casting_info_dict.append(casting_dict)

        shot_list = gazu.casting.get_asset_cast_in(task_asset)
        shot = gazu.shot.get_shot(shot_list[0]['shot_id'])
        seq = gazu.shot.get_sequence_from_shot(shot)
        all_shots = gazu.shot.all_shots_for_sequence(seq)
        for shot in all_shots:
            undi_info_list.append(self._list_append(shot, gazu.files.get_output_type_by_name('Undistortion_img')))  ####output type 이름 바꿔야 함
            camera_info_list.append(self._list_append(shot, gazu.files.get_output_type_by_name('Camera')))

        return casting_info_dict, undi_info_list, camera_info_list

    def get_task_info(self, task):
        """
        작업 유형, 연결된 엔티티, 프로젝트, 시퀀스, 샷 및 할당된 사용자 뿐만 아니라
        시작 날짜, 기한, 상태 및 우선 순위와 같은 다양한 기타 속성을 포함하여 작업에 대한 관련 정보를 검색합니다.

        Args:
            task (dict): 작업 개체를 나타내는 사전입니다.

        Returns:
            dict: 작업에 대한 관련 정보가 들어 있는 사전입니다.
        """
        task_type = gazu.task.get_task_type_by_id(task['task_type_id'])
        entity = gazu.entity.get_entity(task['entity_id'])
        project = gazu.project.get_project(entity['project_id'])
        sequence = gazu.shot.get_sequence(entity['parent_id'])
        shot = gazu.shot.get_shot(entity['id'])
        assignee = gazu.user.get_user(task['assigned_to_id'])

        task_info = {
            'id': task['id'],
            'name': task['name'],
            'task_type': task_type['name'],
            'entity': entity['name'],
            'project': project['name'],
            'sequence': sequence['name'],
            'shot': shot['name'],
            'assignee': assignee['name'],
            'start_date': task['start_date'],
            'due_date': task['due_date'],
            'status': task['status'],
            'priority': task['priority'],
            'description': task['description'],
            'comment': task['comment']
        }

        return task_info

    def _filter_info(self, proj_num=0, seq_num=0):
        """
        유저가 필터링을 했는지 판별하여 해당하는 task들만 노출하는 매서드
        유저가 클릭한 테스크의 dict를 task에 저장한다

        Args:
            proj_num: 선택한 프로젝트의 인덱스 번호. 0은 All을 뜻한다
            seq_num: 선택한 시퀀스의 인덱스 번호. 0은 All을 뜻한다

        Returns:
            list: 필터링된 task(dict)의 집합
            list: 필터링된 task 정보 중 필요한 내용만 담긴 dict의 집합
        """
        task_info_list, task_list, proj_set, seq_set = self._collect_info_task()
        filtered_task_list = []
        filtered_task_info_list = []
        double_filtered_task_list = []
        double_filtered_task_info_list = []
        filtered_seq_set = []

        # 프로젝트 이름 필터링
        if proj_num is 0:
            proj = proj_set
            return task_list, task_info_list
        else:
            proj = proj_set[proj_num-1]
            for index, task in enumerate(task_list):
                if task['project_name'] is proj:
                    filtered_task_list.append(task)
                    filtered_task_info_list.append(task_info_list[index])
            for seq_name in seq_set:
                try:
                    gazu.shot.get_sequence_by_name(proj, seq_name)
                except Exception as exc:
                    continue
                filtered_seq_set.append(seq_name)
            seq_set = filtered_seq_set

        # 프로젝트를 필터링할 시 시퀀스 이름으로도 필터링 가능
        if seq_num is 0:
            seq = seq_set
            return filtered_task_list, filtered_task_info_list
        seq = seq_set[seq_num-1]
        for index, task in enumerate(filtered_task_list):
            if filtered_task_info_list[index]['sequence_name'] is not seq:
                continue
            else:
                double_filtered_task_list.append(task)
                double_filtered_task_info_list.append(filtered_task_info_list[index])
                return double_filtered_task_list, double_filtered_task_info_list

    def select_task(self, proj_num=0, seq_num=0, task_num=None):
        """
        필터링을 마친 뒤 선택한 테스크에 대한 정보를 노출하는 매서드

        Args:
            proj_num: 선택한 프로젝트의 인덱스 번호. 0은 All을 뜻한다
            seq_num: 선택한 시퀀스의 인덱스 번호. 0은 All을 뜻한다
            task_num: 선택한 테스크의 인덱스 번호. 테스크 선택 전에는 None

        Returns:
            dict or list: 선택한 task의 딕셔너리 또는 task의 집합(선택 전)
            list: 선택한 task의 정제된 정보를 담은 리스트
            list: 캐스팅된 에셋의 리스트
            list: 언디스토션 이미지의 리스트
            list: 카메라의 리스트
            list:
        """
        casting_info_list = None
        undi_info_list = None
        camera_info_list = None
        final_task_list, final_task_info_list = self._filter_info(proj_num, seq_num)
        if task_num is None:
            task = final_task_list
            task_info = final_task_info_list
        else:
            task = final_task_list[task_num]
            task_info = final_task_info_list[task_num]
            casting_info_list, undi_info_list, camera_info_list = self._collect_info_casting(task)
        tup = thumbnail_control(task, task_num, casting_info_list, undi_info_list)

        # pp.pprint(task)
        # pp.pprint(task_info)
        # print('cast', casting_info_list)
        # print('undi', undi_info_list)
        # print('cam', camera_info_list)

        return task, task_info, casting_info_list, undi_info_list, camera_info_list, tup

    def select_shot(self, shot_list, shot_num):
        """
        에셋 목록 중 선택한 샷에 캐스팅된 에셋, 언디스토션 이미지, 카메라만 노출하도록 하는 매서드

        Args:
            shot_list(list): 시퀀스에 속한 모든 샷 딕셔너리의 집합
            shot_num(int): 작업할 샷의 인덱스 번호

        Returns:
            dict: 선택한 샷의 딕셔너리가 들어있는 리스트
        """
        undi_info_list = []
        camera_info_list = []
        casting_info_dict = []
        shot = shot_list[shot_num]
        all_casts = gazu.casting.get_shot_casting(shot)
        all_casting_list = all_casts.values()
        for casting_list in all_casting_list:
            for cast in casting_list:
                asset = gazu.asset.get_asset(cast['asset_id'])
                casting_dict = {'asset_name': cast['asset_name'],
                                'description': asset['description'],
                                'asset_type_name': cast['asset_type_name'],
                                'nb_occurences': cast['nb_occurences'],
                                'revision': cast['revision'],
                                'comment': cast['comment']}
                casting_info_dict.append(casting_dict)
        undi_info_list.append(self._list_append(shot, gazu.files.get_output_type_by_name('Undistortion_img')))  ####output type 이름 바꿔야 함
        camera_info_list.append(self._list_append(shot, gazu.files.get_output_type_by_name('Camera')))

        print('cast', casting_info_dict)
        print('undi', undi_info_list)
        print('cam', camera_info_list)
