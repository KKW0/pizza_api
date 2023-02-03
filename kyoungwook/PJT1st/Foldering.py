"""
    Lucidity를 활용하여 스튜디오의 모든 파일 경로를 지정하고 또 추출할 수 있는 코드 (데이터베이스 없이, yaml 또는 json으로 대체)
"""

import lucidity
import json
import os


class FolderingFile:
    def __init__(self):
        """
            1. self._json_path는 탬플릿이 저장될 파일의 경로입니다
            2. self_templates는 빈공간에 json 파일에서 로드된 탬플릿을 저장하는역할입니다
            3. self.template는 빈 공간에 현재 탬플릿을 저장할때 사용됩니다
            4. self.json_load는 json 파일의 탬플릿을 self.t_templates로 로드시키는 역할입니다
        """
        self._json_path = '/home/rapa/PycharmProjects/PJT1/KKW_PJT.json'
        self._templates = {}
        self._template = {}
        self._template_name = None
        self.json_load()


    def add_template(self, nick, pattern):
        """
        self._templates 사전에 새 템플릿을 추가하고 self.json_save를 호출하고 업데이트 된 탬플릿을 json 파일에 저장하며json 파일에 저장되어 언제나 로드가 가능합니다.
        Args:
            nick: nick이라는 key값을 사용하고 탬플릿의 이름입니다.
            pattern: pattern이라는 value를 사용합니다
        """
        self._templates[nick] = pattern
        self.json_save()


    def json_save(self):
        """
           1. self._templates에 저장된 데이터 변수self._json_path의 경로에 파일을 저장합니다
           2. 파일을 쓰기모드로 열고 json.dumpsms self.templates의 내용을 파일을 사용하는데 사용되고
           3. f 변수는 쓸 파일을 json.dump함수에 전달시키며 같은 이름의 파일이 있따면 덮어쓰고 없다면 새 파일을 생성합니다.
        """
        with open(self._json_path, 'w') as f:
            json.dump(self._templates, f)


    def json_load(self):
        """
           1. self._json_path의 저장 경로에 파일이 있는지 확인하며 읽기모드 상태에서 파일을 열고
           2. json.load 함수를 사용해 self._templates를 로드합니다
           3. with open으로 파일을 읽고 닫기를 확인하고 파일이 없다면 아무것도 하지않습니다.
        """
        if os.path.exists(self._json_path):
            with open(self._json_path, "r") as f:
                self._templates = json.load(f)


    def print_templates(self):
        """
           1. self._templates 변수에 저장된 현재 템플릿을 출력합니다.
           2. nick의 key와 pattern의 value를 보여주는 역할입니다.
        """
        print(self._templates)

    @property
    def template_name(self):
        """
        Returns: 속성을 정의하고 template_name의 값을 반환하고 메서드가 읽기전용이여야 함을 보여줍니다
        """
        return self._template_name

    @template_name.setter
    def template_name(self, value):
        """
        Args:
            value: value는 인자값이며 탬플릿 이름입니다.
        Raise: 메서드가 _templates에 있는지 확인하며 그렇지 않은경우 valueError을 발생시킵니다
        """
        if value not in self._templates:
            raise ValueError("Error: 없는 탬플릿을 입력했습니다 다시 입력해주세요.")
        self._template_name = value
        self.set_template(value)

    def set_template(self, nick):
        """
        self._templates에서 해당 탬플릿에 엑세스하고 클래스의 인스턴스를 생성해주고 탬플릿을 생성합니다
        Args:
            nick: 탬플릿의 이름이자 변수이며 입력값입니다. 인수로서 전달되며 nick이 self._templates에 없는 경우 에러 메시지를 출력하도록 설정되어 있습니다.
        """
        # if nick not in self._templates:
        #     print("Error: 없는 탬플릿을 입력했습니다 다시 입력해주세요.")
        #     return
        temp = self._templates[nick]
        self._template = lucidity.Template(nick, temp)

    def set_path(self, path):
        """
            제공된 경로가 없거나 틀릴경우 애러메시지를 출력하며 메서드는 추출된 데이터를 리턴합니
        Args:
            path: 파일의 경로를 입력받아 해당 경로의 파일을 읽어들여 탬플릿과 비다교하여 필요한 데이터를 추출합니다.
        Returns: set_path에서 사용되는 변수로 path로 전달된 파일 경로를 통해 데이터를 저장하고 반환합니
        """
        if not path or not os.path.exists(path):
            raise ValueError("잘못된 파일 경로가 제공되었습니다. 다시 입력해주세요 : {}".format(path))
        # self_path = path
        data = self._template.parse(path)
        return data
        # index_list = list(self_data.items())
        # for parsing in index_list:
        #     print(parsing)

def main():
    """
       1. sf.print_templates() 는 클래스에 저장된 탬플릿을 추출해줍니다
       2. sf.set_template('') 는 ('') 안에있는 탬플릿을 현재 탬플릿으로 설정합니다
       3. sf.set_path('') 는 ('')안에 설정된 경로를 호출하여 현재 탬플릿의 경로로 설정합니다.
       4. sf.add_template('') 는 새 탬플릿을 추가 해주는 기능입니다 ('') 안에 추가하고싶은 매개변수 키 , 값 을 넣어 사용해주세요
       5. sf.json_save() 탬플릿을 json파일에 저장하는 역할을 수행합니다.
    """
    sf = FolderingFile()
    sf.print_templates()
    sf.template_name = "kangkyoungwook1"
    # sf.set_template('kangkyoungwook1')
    data = sf.set_path('/home/rapa/project/avata/shot/boo/0010/plate/v001/boo_0010_plate_v001.0010.jpg')
    print(data)
    # sf.add_template("kangkyoungwook3", '/home/rapa/project/{project}/shot/{seq}/{shot}/{dept}/{ver}/{seq}_{shot}_{dept}_{ver}.{padding}.{ext}')
    # sf.json_save()
    print(data["project"])

if __name__ == "__main__":
    main()