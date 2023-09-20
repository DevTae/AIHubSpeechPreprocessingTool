# Developed by DevTae@2023
# 모든 데이터셋을 다 압축 해제하였다면 각각의 데이터셋에 대한 메타데이터를 만들어야 한다.
# 135.명령어_인식을_위한_소음_환경_데이터 를 예시로 작성한 함수임.
# 각자의 데이터셋에 맞게 해당 파이썬 코드를 수정하여 각 데이터셋의 최상 디렉토리 안에 넣고 사용하면 된다.

import os
import json


test = False # 테스트를 위하여 반복문 한 개만 실행


# 특정 확장명을 바탕으로 모든 라벨링 데이터 path 리스트를 불러온다. 
def get_label_path_list(root_path: str):
    ext = ".json" # 라벨링 데이터 확장명
    
    list_of_label_path = list()
    
    if test is True:
        is_break = False
    
    for (root, _, files) in os.walk(root_path):
        print("[get_label_path_list]", root, "디렉토리를 탐색 중입니다.")
    
        if test is True:
            if is_break is True:
                break
            
        for file in files:
            if file.endswith(ext):
                list_of_label_path.append(os.path.join(root, file))
                
                if test is True:
                    is_break = True
                    break
                
    return list_of_label_path


# 한 개의 라벨 path 를 바탕으로 오디오 path 와 라벨링 데이터로 변환한다.
def get_audio_path_and_transcript_from_label_path(label_path):
    
    with open(label_path, 'r') as f:
        content = f.read()
        content = json.loads(content)
    
    # audio path 정의
    audio_path = label_path.replace("TL", "TS")
    audio_path = audio_path.replace("VL", "VS")
    audio_path = audio_path.replace("02.라벨링데이터", "01.원천데이터")
    audio_path = os.path.dirname(audio_path)
    audio_path = os.path.join(audio_path, content['file']['name'])
    audio_path = audio_path + ".wav"
    
    audio_path_n = audio_path.replace(".wav", "-N.wav")
    audio_path_s = audio_path.replace(".wav", "-S.wav")
        
    transcript = content['command']['text']

    # Sampling Rate 및 오디오 길이 확인하는 과정 (제외 프로세스)
    if content['file']['length'] != content['file']['speechLength']:
        return None, None, None
    elif content['file']['samplingRate'] != '16kHz':
        return None, None, None
    
    # 해당 부분 audio_path 를 2 개 반환하도록 수정할 수 있음
    return audio_path_n, audio_path_s, transcript


# 라벨 파일들을 바탕으로 audio file path 리스트와 transcripts 리스트를 불러온다.
def write_metadata_from_label_path_list(list_of_label_path):
    
    with open("metadata.txt", 'w') as f:
    
        for label_path in list_of_label_path:
            audio_path_n, audio_path_s, transcript = get_audio_path_and_transcript_from_label_path(label_path)
            
            f.write(audio_path_n + "\t" + transcript + "\n")
            f.write(audio_path_s + "\t" + transcript + "\n")
            
            print("[write_metadata_from_label_path_list]", label_path, "파일에 대하여 작성 완료하였습니다.")
    

if __name__ == "__main__":
    print("해당 디렉토리에 대하여 메타데이터 전처리를 진행합니다.")
    list_of_label_path = get_label_path_list(os.getcwd())
    write_metadata_from_label_path_list(list_of_label_path)
    print("해당 디렉토리에 대한 메타데이터 전처리를 완료하였습니다.")
    
