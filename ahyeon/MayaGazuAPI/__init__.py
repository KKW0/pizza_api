# coding:utf8
import gazu
"""
프로젝트에서 사용자에게 주어진 테스크 중 하나를 선택하고,
테스크가 소속된 샷에 캐스팅되어 있는 에셋 데이터를 가져오고,
각 에셋의 working file과 output file을 추출하여,
씬에 import 해서 레이아웃 작업을 한 뒤에,
작업한 working file과 output file을 실제 폴더 트리에 저장하고,
그것들을 Kitsu에 퍼블리싱하고, working file을 업로드도 해주는 클래스
Layout 팀을 위한 api
"""



from kitsumaya import SetThings