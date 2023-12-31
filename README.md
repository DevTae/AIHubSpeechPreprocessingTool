### AIHub Speech Preprocessing Tool

- AI-Hub 데이터셋을 바탕으로 음성 모델 훈련을 진행하고자 하는 사람들을 위하여 전처리 툴을 만들게 되었다.

<br/>

- 실행 환경 : Ubuntu 20.04

- 다음 과정으로 진행하면 전처리를 쉽게 완료할 수 있다.

  - 실제 데이터셋을 예시로 들어 설명하고자 한다.

  - 우선, 폴더 구조는 다음과 같다고 가정하자.
  
  ```
  📦AIHubSpeechPreprocessingTool
   ┣ 📂preprocess
   ┣ 📂135.명령어_인식을_위한_소음_환경_데이터
   ┃ ┣ 📂01.데이터
   ┃ ┃ ┣ 📂Training
   ┃ ┃ ┃ ┣ 📂01.원천데이터
   ┃ ┃ ┃ ┃ ┣ 📄TS_01.다화자_소음_환경_001.식당_01.원거리.tar.gz
   ┃ ┃ ┃ ┃ ┗  ...
   ┃ ┃ ┃ ┗ 📂02.라벨링데이터
   ┃ ┃ ┃   ┣ 📄TL_01.다화자_소음_환경_001.식당_01.원거리.tar.gz
   ┃ ┃ ┃   ┗  ...
   ┃ ┃ ┗ 📂Validation
   ┃ ┃   ┣ 📂01.원천데이터
   ┃ ┃   ┃ ┣ 📄VS_01.다화자_소음_환경_001.식당_01.원거리.tar.gz
   ┃ ┃   ┃ ┗  ...
   ┃ ┃   ┗ 📂02.라벨링데이터
   ┃ ┃     ┣ 📄VL_01.다화자_소음_환경_001.식당_01.원거리.tar.gz
   ┃ ┃     ┗  ...
   ┃ ┣ 📄2.make_metadata_each.py
   ┃ ┗ 📄metadata.txt
   ┣ 📂...
   ┣ 📄1.make_extract_all_sh.py
   ┣ 📄2.make_metadata_each.py
   ┣ 📄3.make_metadata_total.py
   ┣ 📄4.make_metadata_total_balanced.py
   ┣ 📄extract_all.sh
   ┗ 📄README.md
  ```

<br/>

1. 다음과 같이 `1.make_extract_all_sh.py` 파일과 `2.make_metadata_total.py` 파일과 `3.make_metadata_total.py` 파일, 그리고 `4.make_metadata_total_balanced.py` 파일을 모두 제 위치에 맞게 위치한다.

2. `$ cd AIHubSpeechPreprocessingTool`

3. `$ python make_extract_all_sh.py`

    - 다음 커맨드를 진행하면 해당 디렉토리를 포함하여 모든 하위 폴더에 있는 모든 압축 파일들에 대하여 압축 해제할 수 있는 sh 파일이 생성된다.

    - `extract_all.sh` 이라는 이름으로 모든 압축 파일들의 압축 해제를 자동으로 진행하는 배치 파일이 생성된다.

    - 현재 압축이 끝난 파일에 대해서는 자동으로 삭제하는 기능을 추가하였다.

4. `$ bash extract_all.sh`

    - 다음과 같이 모든 압축 파일들의 압축 해제를 진행한다.

5. `$ cp 2.make_metadata_each.py 135.명령어_인식을_위한_소음_환경_데이터/`

    - 다음과 같이, 각 데이터셋들에 `📄2.make_metadata_each.py` 파일을 복사한다.

6. 각 디렉토리에 대하여 다음과 같이, `$ cd 135.명령어_인식을_위한_소음_환경_데이터 && python 2.make_metadata_each.py` 를 진행한다.

    - **(핵심!!)** 각 데이터셋마다 metadata 의 구조가 다르기 때문에 그에 맞게 수정 과정을 거치고 사용해야 한다.

    - 실행한 결과, 각 디렉토리들에 `📄metadata.txt` 파일들이 저장된다.
      
    - 다음 형식을 바탕으로 전처리가 되도록 하였다.
      - `{음성 상대 주소}\t{음성 Transcript}\n`

7. `📦AIHubSpeechPreprocessingTool` 디렉토리에서 `python 3.make_metadata_total.py 135.명령어_인식을_위한_소음_환경_데이터/metadata.txt metadata.txt` 를 실행한다.

    - 더 자세한 사용법은 다음과 같다.
      - `python 3.make_metadata_total.py {병합할 metadata.txt} {병합할 metadata.txt} ... {모두 합쳐진 metadata.txt}`

    - 그 결과, 모든 내용이 합쳐진 `📄metadata.txt` 파일을 만들어낼 수 있다.

8.  `📦AIHubSpeechPreprocessingTool` 디렉토리에서 `python 4.make_metadata_total_balanced.py metadata.txt` 를 실행한다.

    - 추가적으로, `📄metadata.txt` 에서 다양한 데이터셋이 `균등 분포` 를 이룰 수 있도록 데이터 선정 알고리즘을 적용한다.

9. 최종적으로 만들어진 `📄metadata.txt` 파일을 바탕으로 `KoSpeech` 혹은 `OpenSpeech` 등의 음성 모델 툴킷을 활용하여 학습을 진행할 수 있다.

10. **(KoSpeech 및 OpenSpeech 한정)** `📦preprocess` 디렉토리에서 `bash preprocess.sh` 를 실행하여 만들어진 단어사전에 매핑한 최종 라벨 데이터를 생성할 수 있다.

    - `preprocess.sh` 에서 데이터셋과 `metadata.txt` 가 있는 경로를 설정할 수 있다.
    - 만약, 오류가 난다면 `pip install -r requirements.txt` 를 실행하도록 하자.

<br/>

- AI-Hub 를 활용하여 음성 딥러닝 프로젝트를 진행할 때, 매번 똑같은 과정을 진행하던 중 반복되는 수작업을 줄이기 위하고자 해당 코드들을 작성하게 되었고, 저와 비슷한 사람들에게 도움이 되고자 업로드하게 되었습니다.

<br/>

#### 참조

- [명령어 인식을 위한 소음 환경 데이터](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=71405)
- [sooftware/kospeech](https://github.com/sooftware/kospeech)
- [stannam/hangul_to_ipa](https://github.com/stannam/hangul_to_ipa)
  
