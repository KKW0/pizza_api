#coding:utf8

import gazu
import pprint as pp


class Filter:
    def __init__(self):
        # gazu.client.set_host("http://192.168.3.116/api")
        # gazu.log_in("keiel0326@gmail.com", "tmvpdltm")
        # gazu.client.set_host("http://192.168.3.116/api")
        # gazu.log_in("pipeline@rapa.org", "netflixacademy")
        self.seq = None

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
        asset = gazu.asset.get_asset(task['entity_id'])
        shots = gazu.casting.get_asset_cast_in(asset)
        shot = gazu.shot.get_shot(shots[0]['shot_id'])
        self.seq = gazu.shot.get_sequence_from_shot(shot)
        task_info['sequence_name'] = self.seq['name']

        return task_info, self.seq['name']

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
        task_list = []
        task_info_list = []
        sort_dict = dict()
        tmp_task_list = gazu.user.all_tasks_to_do()
        for index, task in enumerate(tmp_task_list):
            if task['task_type_name'] == 'LayoutPizza':
                proj_list.append(task['project_name'])
                task_info, seq_name = self._get_information_dict(task)
                sort_dict[task['project_name']] = seq_name
                task_info_list.append(task_info)
                task_list.append(task)
                seq_list.append(seq_name)
        proj_set = list(set(proj_list))
        seq_set = list(set(seq_list))

        return task_info_list, task_list, proj_set, seq_set, sort_dict

    def _list_append(self, shot, output_type):
        """
        리스트에 아웃풋 파일(언디스토션 이미지, camera)의 정보를 담는다

        Args:
            shot(dict): 언디스토션 이미지, 카메라의 아웃풋 파일이 속한 shot
            output_type(dict): 아웃풋 파일이 속한 아웃풋 타입(jpg, abc )

        Returns:
            list: output file의 모델에서 필요한 정보들만 담은 리스트의 집합
        """
        info_list = []
        task_type = gazu.task.get_task_type_by_name('Matchmove')
        aa = gazu.files.get_last_output_files_for_entity(shot['id'], output_type, task_type)
        output_list = gazu.files.get_last_output_files_for_entity(shot['id'], output_type, task_type)
        output_dict = dict()
        output_dict['output_type_name'] = output_type['name']
        if len(output_list) is 0:
            raise ValueError("해당하는 output file이 존재하지 않습니다.")
        for output in output_list:
            output_dict['output_name'] = output['name']
            output_dict['comment'] = output['comment']
            output_dict['description'] = output['description']
            info_list.append(output_dict)

        return info_list

    def _cast_dict_append(self, cast, output_type, asset, task_type):
        """
        캐스팅 정보가 담긴 딕셔너리의 집합을 리턴하는 매서드

        Args:
            cast:
            output_type(list): 에셋에서 쓰이는 아웃풋 타입의 집합
            asset:
            task_type:

        Return:
        """
        output_list = []
        output_dict = {'output_type': None,
                       'revision': None,
                       'representation': None,
                       'description': None
                       }
        for item in output_type:
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
        task_type = gazu.task.get_task_type(task['task_type_id'])
        shot_list = gazu.shot.all_shots_for_sequence(self.seq['id'])
        asset = gazu.entity.get_entity(task['entity_id'])
        all_casting_list = gazu.casting.get_asset_casting(asset)
        for cast in all_casting_list:
            casted_asset = gazu.asset.get_asset(cast['asset_id'])
            output_types = gazu.files.all_output_types_for_entity(casted_asset)
            casting_dict = self._cast_dict_append(cast, output_types, casted_asset, task_type)
            casting_info_list.append(casting_dict)
        for shot in shot_list:
            jpgs = gazu.files.get_output_type_by_name('UndistortionJpg')
            abc = gazu.files.get_output_type_by_name('Alembic')
            if self._list_append(shot, jpgs):
                undi_info_list.append(self._list_append(shot, jpgs))
            if self._list_append(shot, abc):
                camera_info_list.append(self._list_append(shot, abc))

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
        task_info_list, task_list, proj_set, seq_set, _ = self._collect_info_task()
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
        return task, task_info, casting_info_list, undi_info_list, camera_info_list

# gazu.client.set_host("http://192.168.3.116/api")
# gazu.log_in("keiel0326@gmail.com", "tmvpdltm")
# proj = gazu.project.get_project_by_name('Project1')
# seq = gazu.shot.get_sequence_by_name(proj, 'seq1')
# shots = gazu.shot.get_shot_by_name(seq, 'sh1')
# ft = Filter()
# jpg = gazu.files.get_output_type_by_name('UndistortionJpg')
# a = ft._list_append(shots, jpg)
# pp.pprint(a)