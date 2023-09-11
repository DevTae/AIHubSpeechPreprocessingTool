# Developed by DevTae@2023
# 모든 데이터셋에 대하여 metadata.txt 를 만들었다면 모든 metadata 를 통합한다.
# `python make_metadata_total.py dataset1/metadata.txt dataset2/metadata.txt metadata.txt` 를 바탕으로 실행할 수 있다.
# ./dataset1/metadata.txt 와 ./dataset2/metadata.txt 를 합쳐 ./metadata.txt 을 작성한다.
# 이전 make_metadata_each.py 를 바탕으로 절대주소를 작성하였고, 해당 코드를 통해 다른 환경에서도 활용 가능하도록 상대주소로 변환한다.

import os
import sys
import json


def write_all_metadata(list_of_metadata, result_of_metadata):
    root_path = os.path.join(os.getcwd(), result_of_metadata)
    root_path = os.path.dirname(root_path)

    with open(result_of_metadata, "w") as f:
        for metadata in list_of_metadata:
            with open(metadata, "r") as meta_f:
                for line in meta_f.readlines():
                    if line == "\n":
                        continue

                    for idx, elem in enumerate(line.split('\t')):
                        if idx == 0:
                            f.write(os.path.relpath(elem, root_path)) # 상대주소 작성
                        else:
                            f.write("\t" + elem)
        
        
if __name__ == "__main__":
    list_of_metadata = sys.argv[1:-1]
    result_of_metadata = sys.argv[-1]
    
    if os.path.isfile(result_of_metadata):
        print("이미 파일이 존재합니다. 다른 이름으로 작성해주세요.")
        exit()
    
    for metadata in list_of_metadata:
        if not os.path.isfile(metadata):
            print("형식에 맞지 않는 파일이 입력되었습니다.")
            exit()
    
    print("전처리 통합 과정을 시작하였습니다.")
    write_all_metadata(list_of_metadata, result_of_metadata)
    print("전처리 통합 과정을 완료하였습니다.")

