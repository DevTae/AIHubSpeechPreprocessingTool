# Developed by DevTae@2023
# 통합된 metadata 를 그대로 사용하지 않고 원하는 데이터 개수를 바탕으로 균등 분포 형태로 구성하도록 한다.

import os
import sys
import shutil
import random
import datetime


def explore_directories(metadata_filename) -> [ dict, dict ]:
    # metadata 파일을 바탕으로 폴더에 대한 정보를 파악한다.
    folder_tree = dict()
    folder_tree_count = dict()
    
    with open(metadata_filename, "r", encoding='utf8') as f:
        for line in f.readlines():
            file_path = line.split('\t')[0]
            folder_names = file_path.split('/')[:-1] # 파일 제외
    
            # 포인터로서 사용
            pointer = folder_tree
    
            for idx, folder_name in enumerate(folder_names):
                if folder_name not in pointer.keys():
                    pointer[folder_name] = dict()
    
                path = '/'.join(folder_names[0:idx+1])
    
                if path not in folder_tree_count.keys():
                    folder_tree_count[path] = [ 1, 0 ] # [ 총 개수, 선택된 개수 ]
                else:
                    folder_tree_count[path][0] += 1
    
                pointer = pointer[folder_name]
    
    return folder_tree, folder_tree_count


# 데이터 크기를 균형적으로 나눠주는 재귀 함수
# 특정 부분만 라벨링이 적을수도 있기 때문에, 전체적인 흐름에서 봤을 때 균등 분포를 이루기만 한다면 괜찮도록 진행.
def divide_files(pointer: dict, folder_tree_count: dict, size: int, now_path: str, filter_keywords: list):
    # 종료 조건
    if len(list(pointer.values())) == 0:
        folder_tree_count[now_path][1] = size
        return

    # 예외 처리 진행
    folders = list(pointer.values())
    filtered = False

    for folder in folders:
        for filter_keyword in filter_keywords:
            if filter_keyword in str(folder).lower():
                filtered = True

    # 필터링된 부분에 있어서는 데이터 개수가 그대로 이어짐
    if filtered is True:
        divided_size = size
    else:
        divided_size = int(size / len(pointer.keys()))
        
    # 각 keys 자식들에 대한 재귀 함수 호출 진행
    for key in pointer.keys():
        # prev_path, now_path 설정
        if now_path == '':
            next_path = str(key)
        else:
            next_path = str(now_path) + '/' + str(key)
        
        divide_files(pointer[key], folder_tree_count, divided_size, next_path, filter_keywords)


# 현재 폴더 구조 상황에서 추천하는 데이터 개수를 알려줌
# 데이터셋마다 데이터 개수가 다를 때 쓰기 좋은 방법임
def recommended_data_size(pointer: dict):
    min_of_count = 999999999 # 최댓값

    for key in pointer.keys():
        min_of_count = min(min_of_count, folder_tree_count[list(pointer.keys())[0]][0])

    return min_of_count * len(pointer.keys())


# 선정된 데이터에 대한 개수들을 출력함
def show_count(folder_tree_count: dict):
    for key in folder_tree_count.keys():
        if folder_tree_count[key][1] != 0:
            print(key,folder_tree_count[key][1])


# 선정된 데이터를 다시금 metadata 에 쓴다.
def write_metadata(metadata_filename_in, metadata_filename_out, folder_tree_count):
    with open(metadata_filename_out, 'w', encoding='utf8') as f_w:
        with open(metadata_filename_in, 'r', encoding='utf8') as f_r:
            for line in f_r.readlines():
                if line == '\n':
                    break
                file_path = line.split('\t')[0]
                folder_path = '/'.join(file_path.split('/')[:-1])
                if folder_path in folder_tree_count.keys():
                    if folder_tree_count[folder_path][1] > 0:
                        f_w.write(line)
                        folder_tree_count[folder_path][1] -= 1


if __name__ == "__main__":
    # 경로 지정
    metadata_filename = sys.argv[-1]
    metadata_backup_filename = metadata_filename.replace(".txt", "_") + datetime.datetime.today().strftime('%Y%m%d%H%M%S') + ".txt"

    # 원본의 metadata 를 백업한다.
    shutil.copyfile(metadata_filename, metadata_backup_filename)

    # 현 디렉토리를 탐색한다.
    folder_tree, folder_tree_count = explore_directories(metadata_backup_filename)

    # 탐색한 디렉토리 구조를 바탕으로 추천하는 데이터 크기를 구한다.
    data_size = recommended_data_size(folder_tree)
    print("[notice] 현재 탐색한 결과, 데이터 크기를 ", data_size, "까지 고를 수 있습니다.")

    data_size = int(input("[input] 원하는 데이터 개수를 입력해주세요. : "))

    # 최상위 디렉토리를 시작으로 최하위 디렉토리까지 데이터를 균형적으로 나눈다.
    filter_keywords = [ "train", "valid" ] # 필터링할 쌍의 디렉토리 이름 (소문자로만)
    divide_files(folder_tree, folder_tree_count, data_size, '', filter_keywords)

    # 선정된 데이터에 대한 개수를 출력한다.
    show_count(folder_tree_count)

    # 선정된 데이터에 대하여 메타데이터를 새로 작성한다.
    write_metadata(metadata_filename_in=metadata_backup_filename,
                   metadata_filename_out=metadata_filename,
                   folder_tree_count=folder_tree_count)

    print("[notice] 메타데이터 전환이 완료되었습니다.")

