"""
이 패키지는 Lucidity를 활용하여 스튜디오의 모든 파일 경로를 지정하고, 추출할 수 있습니다. (json으로 작성되었습니다.)
"""
"""
                                         패키지사용법
    1. sf.print_templates()를 사용하여 현재 저장되어있는 탬플릿을 보고 어떠한 탬플릿을 선택할지 골라주세요
    
    2. 고르신 탬플릿의 이름을 sf.template_name에 작성해주세요 , 마음에 드는 탬플릿이 없다면 아래 예시를 참고하여 탬플릿을 추가해주세요
    
    ex) sf.add_template("kangkyoungwook3", '/home/rapa/project/{project}/shot/{seq}/{shot}/{dept}/{ver}/{seq}_{shot}_{dept}_{ver}.{padding}.{ext}') 
                        원하는 탬플릿의 이름                                        원하는 방식의 패턴
                        
    3. data = sf.set_path('/home/rapa/project/avata/shot/boo/0010/plate/v001/boo_0010_plate_v001.0010.jpg')
       data값을 사용하여 원하시는 키값을 입력해주세요 아래 예시를 참고해주세요
       
    ex)print(data["project"]),
       print(data["seq"]),
       print(data["shot"]),
       print(data["dept"]),
       print(data["ver"]),
       print(data["padding"]),
       print(data["ext"])
"""