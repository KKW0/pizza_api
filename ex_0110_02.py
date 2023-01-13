# projectname seqname shotname version frame path 나오도록 만들어보자

import os
import csv

path = '/home/rapa/yehunHwang/project'


# words = path.split("/")
# print(words)


def path_print():
    """
    경로를 받는 함수, .jpg 가 포함 된 것들만 받음
    """
    abs_path_list = []
    for roots, dirs, files in os.walk(path):        
        # for dir_name in dirs:
        #     abs_path = os.path.join(roots, dir_name)            
        #     print(abs_path)
        
        for file_name in files:
            abs_path = os.path.join(roots, file_name)
            abs_path_list.append(abs_path)
            # print(abs_path)
    return abs_path_list


def slice_path(file_list):
    """
    경로 받은 데이터를 쪼개는 함수
    """
    words_list = []
    for line in file_list:
        words = line.split("/")
        words_list.append(words)
        # print(words)
        
    return words_list


def csv_wrting(input_words):
    """
    받은 데이터를 CSV에 넣는 함수
    """
    csv_path = os.path.expanduser('~/yehunHwang/exercises/ex_0110_02.csv')
    # print(input_words)
    
    with open(csv_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Project", "Sequence", "Shot", "Version", "Filename"])
        for path_list in input_words:
            project = path_list[5]
            seq = path_list[7]
            shot = path_list[8]
            ver = path_list[10]
            path = path_list[11]
            writer.writerow([project, seq, shot, ver, path])
            # writer.writerow(path_list)
    #     # writer.writerow(input_words)  
    #     writer.writerow(input_words[0][1:])
    #     writer.writerow(input_words[1][1:])
    #     writer.writerow(input_words[2][1:])

    # with open(csv_path, 'w') as f:
    #     writer = csv.writer(f)
    #     for i in 
    #         writer.writerow(input_words[i][1:])
        
     
        


file_list = path_print()

input_words = slice_path(file_list)
csv_wrting(input_words)









# 내가 해본거, 비효율적이라 사용 안함 walk 사용하는방법으로 시도
# def value_print():
#     """
#     값을 출력해줌
#     """
#     for path_value in os.listdir(path):
#         print(path_value)
#         full_path_value = os.path.join(path, path_value)
#         print(full_path_value)
        
#         is_value = os.path.isdir(full_path_value)
#         print(is_value)
        
#         # for s_path_value in os.listdir(full_path_value):
#         #     print(s_path_value)
#         #     s_full_path_value = os.path.join(full_path_value, s_path_value)
#         #     print(s_full_path_value)
#     return

# def search_print():
#     """ 
#     폴더들을 검색하면서 경로를 출력해줌
#     """
#     if os.path.isdir(path):
#         children = os.listdir(path)
#         print(children)
#         for child in children:
#             child_path = os.path.join(path, child)
#             print(child_path)
#     return


# search_print()