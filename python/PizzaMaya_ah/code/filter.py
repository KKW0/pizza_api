# coding:utf8

import gazu
import pprint as pp


class Filter:
    def __init__(self):
        pass

    def _get_information_dict(self, task):
        """
        각 task에서 필터링에 필요한 정보들을 추출하여 딕셔너리에 추가하는 매서드

        _collect_info_task 에서 사용된다.

        Args:
            task(dict): 유저에게 할당된 task

        Returns:
            dict: task에서 필요한 정보만 추출하여 모은 딕셔너리
            str: task asset이 속한 시퀀스의 이름
        """
        task_info = dict()
        task_info['project_name'] = task['project_name']
        task_info['due_date'] = task['due_date']
        task_info['description'] = task['description']
        task_info['last_comment'] = task['last_comment']
        # task asset이 사용되는 seq 구하기
        asset = gazu.asset.get_asset(task['entity_id'])
        shots = gazu.casting.get_asset_cast_in(asset)
        shot = gazu.shot.get_shot(shots[0]['shot_id'])
        seq = gazu.shot.get_sequence_from_shot(shot)
        task_info['sequence_name'] = seq['name']

        return task_info, seq['name']

    def collect_info_task(self):
        """
        필터링에 필요한 프로젝트 이름, 시퀀스 이름을 proj_set, seq_set에 중복 없이 모으고,
        각 task의 정보를 모아 반환하는 매서드

        Returns:
            list(task_info_list): task의 정보들 중 사용자에게 노출할 정보들만 모은 딕셔너리의 집합
                                  keys - project_name, due_date, description, last_comment, sequence_name
            list(task_list): 사용자에게 assign되었고, task status가 _Todo_ 또는 WIP인  모든 task 딕셔너리의 집합
            list(proj_set): 각 task가 속한 프로젝트의 이름들을 중복없이 모든 리스트
            list(seq_set): 각각 task가 속한 프로젝트의 이름들을 중복없이 모은 리스트
        """
        seq_list = []
        proj_list = []
        task_list = []
        task_info_list = []
        sort_dict = dict()
        tmp_task_list = gazu.user.all_tasks_to_do()
        for index, task in enumerate(tmp_task_list):
            if task['task_type_name'] == 'LayoutPizza':
                proj_list.append(task['project_name'])
                task_info, seq_name = self._get_information_dict(task)
                if type(sort_dict.get(task['project_name'])) is list:
                    sort_dict[task['project_name']].append(seq_name)
                else:
                    sort_dict[task['project_name']] = [seq_name]
                task_info_list.append(task_info)
                task_list.append(task)
                seq_list.append(seq_name)
        proj_set = list(set(proj_list))
        seq_set = list(set(seq_list))

        return task_info_list, task_list, proj_set, seq_set, sort_dict

    def _list_append(self, shot, output_type, task_type):
        """
       리스트에 아웃풋 파일(언디스토션 이미지, camera)의 정보를 담는 매서드

        Args:
            shot(dict): 언디스토션 이미지, 카메라의 아웃풋 파일이 속한 shot
            output_type(dict): 아웃풋 파일이 속한 아웃풋 타입(jpg, abc )
            task_type:

        Returns:
            list: output file의 모델에서 필요한 정보들만 담은 리스트의 집합드
        """
        info_list = []
        output_list_tmp = gazu.files.get_last_output_files_for_entity(shot['shot_id'], output_type, task_type)
        output_list_tmp2 = output_list_tmp
        output_list = []
        if len(output_list_tmp) > 1:
            for index in range(len(output_list_tmp)):
                del output_list_tmp2[index]
                if len(output_list_tmp2) == 0:
                    break
                for index2 in range(len(output_list_tmp2)):
                    if output_list_tmp[index]['source_file_id'] == output_list_tmp2[index2]['source_file_id']:
                        break
                    else:
                        output_list.append(output_list_tmp[index])
        else:
            output_list = output_list_tmp

        output_dict = dict()
        output_dict['output_type_name'] = output_type['name']
        if len(output_list) is 0:
            raise ValueError("해당하는 output file이 존재하지 않습니다. Shot: {0}".format(shot['shot_name']))
        for output in output_list:
            shot = gazu.shot.get_shot(output['entity_id'])
            output_dict['frame_range'] = shot['nb_frames']
            output_dict['output_name'] = output['name']
            output_dict['comment'] = output['comment']
            output_dict['description'] = output['description']
            output_dict['shot_name'] = shot['name']
            info_list.append(output_dict)

        return info_list

    def _cast_dict_append(self, cast, output_type, asset, task_type):
        """
        캐스팅 정보가 담긴 딕셔너리의 집합을 리턴하는 매서드

        Args:
            cast: 에셋의 캐스팅 info
            output_type(list): 에셋에서 쓰이는 아웃풋 타입의 집합
            asset: a casted asset
            task_type: for get output file (Modeling)

        Return:
        """
        output_list = []
        output_dict = dict()
        for item in output_type:
            is_output = gazu.files.get_last_output_files_for_entity(asset, task_type=task_type)
            if len(is_output) != 0:
                revision = gazu.files.get_last_entity_output_revision(asset, item, task_type)
                output_dict['output_type'] = item['name']
                output_dict['revision'] = revision
                output_list.append(output_dict)
        casting_dict = {'asset_name': asset['name'],
                        'description': asset['description'],
                        'asset_type_name': asset['asset_type_name'],
                        'nb_occurences': cast['nb_occurences'],
                        'output': output_list,
                        }

        return casting_dict

    def _collect_info_casting(self, task):
        """
        선택한 task가 속한 asset(task asset)에 casting된 에셋들의 정보 중 필요한 내용을 추출하여 저장한다.
        task asset이 캐스팅된 샷의 언디스토션 이미지와 camera output의 정보 중 필요한 내용을 추출한다.

        Args:
            task(dict): 선택한 task의 딕셔너리

        Returns:
            list(casting_info_list): 캐스팅된 에셋들의 정보를 담은 리스트의 집합
                                     (asset name, description, asset type name, nb_occurences)
            list(undi_info_list): task asset이 캐스팅된 샷의 언디스토션 이미지 정보를 담은 리스트의 집합
                                 (output name, output type name, comment, description)
            list(camera_info_list): task asset이 캐스팅된 샷의 카메라 정보를 담은 리스트의 집합
                                    (output name, output type name, comment, description)
        """
        casting_info_list = []
        undi_info_list = []
        camera_info_list = []
        task_type = gazu.task.get_task_type_by_name('Modeling')
        task_match = gazu.task.get_task_type_by_name('Matchmove')
        task_cam = gazu.task.get_task_type_by_name('Camera')
        asset = gazu.entity.get_entity(task['entity_id'])
        shot_list = gazu.casting.get_asset_cast_in(asset)
        all_casting_list = gazu.casting.get_asset_casting(asset)
        for cast in all_casting_list:
            casted_asset = gazu.asset.get_asset(cast['asset_id'])
            output_types = gazu.files.all_output_types_for_entity(casted_asset)
            casting_dict = self._cast_dict_append(cast, output_types, casted_asset, task_type)
            casting_info_list.append(casting_dict)
        for shot in shot_list:
            jpgs = gazu.files.get_output_type_by_name('UndistortionJpg')
            abc = gazu.files.get_output_type_by_name('FBX')     ##### Alembic...
            if self._list_append(shot, jpgs, task_match):
                undi_info_list.append(self._list_append(shot, jpgs, task_match))
            if self._list_append(shot, abc, task_cam):
                camera_info_list.append(self._list_append(shot, abc, task_cam))

        return casting_info_list, undi_info_list, camera_info_list

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
        task_info_list, task_list, proj_set, seq_set, _ = self.collect_info_task()
        filtered_task_list = []
        filtered_task_info_list = []
        double_filtered_task_list = []
        double_filtered_task_info_list = []
        filtered_seq_set = []

        # 프로젝트 이름 필터링
        if proj_num == 0 or proj_num == None:
            return task_list, task_info_list
        else:
            proj = proj_set[proj_num-1]
            proj_dict = gazu.project.get_project_by_name(proj)
            for index, task in enumerate(task_list):
                if task['project_name'] == proj:
                    filtered_task_list.append(task)
                    filtered_task_info_list.append(task_info_list[index])
            for seq_name in seq_set:
                if gazu.shot.get_sequence_by_name(proj_dict, seq_name):
                    filtered_seq_set.append(seq_name)
                else:
                    continue
            seq_set = filtered_seq_set

        # 프로젝트를 필터링할 시 시퀀스 이름으로도 필터링 가능
        if seq_num == 0:
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
        return task, task_info, casting_info_list, undi_info_list, camera_info_list
