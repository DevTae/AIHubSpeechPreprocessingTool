# Author
# Soohwan Kim, Seyoung Bae, Cheolhwang Won, Soyoung Cho, Jeongwon Kwak

DATASET_PATH="/media/milab/SSD1/"		# metadata.txt 와 DATASET_PATH
VOCAB_DEST='./'			# 위와 동일하게 세팅 진행
SAVE_PATH='./'			# 위와 동일하게 세팅 진행
OUTPUT_UNIT='ipa'                                          # you can set character / ipa / subword / grapheme # kor, eng, ipa 모두 상관 없이 ipa 로 설정해도 무관함.
PREPROCESS_MODE='phonetic'                                       # phonetic : 칠 십 퍼센트,  spelling : 70%
VOCAB_SIZE=5000                                                  # if you use subword output unit, set vocab size
LANG='kor_ipa'					# Language : kor / eng / kor_ipa / eng_ipa (원하는 형태로 transcript 가 출력됨)


echo "Pre-process Speech Dataset.."

python main.py \
--dataset_path $DATASET_PATH \
--vocab_dest $VOCAB_DEST \
--savepath $SAVE_PATH \
--output_unit $OUTPUT_UNIT \
--preprocess_mode $PREPROCESS_MODE \
--vocab_size $VOCAB_SIZE \
--lang $LANG \
