import pandas as pd
import re
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 추가할 불용어 리스트
new_stopwords = ['하지','얘기','정도','라','스러워요','스럽네','텐데','싶어서','보면','전혀','곳','나를','않고','팀','자리','없어서','없는','하니까','같은']

# "korean_stopwords.txt" 파일 읽기
stopwords_url = "korean_stopwords.txt"
with open(stopwords_url, 'r', encoding='utf-8') as file:
    existing_stopwords = file.read().splitlines()

# 기존 불용어 리스트에 새로운 불용어 추가
updated_stopwords = existing_stopwords + new_stopwords
updated_stopwords = list(set(updated_stopwords))  # 중복 제거

# 변경된 불용어 리스트를 "korean_stopwords.txt" 파일에 저장
with open(stopwords_url, 'w', encoding='utf-8') as file:
    for stopword in updated_stopwords:
        file.write(stopword + '\n')

# 불용어 처리 함수 "https://raw.githubusercontent.com/yoonkt200/FastCampusDataset/master/korean_stopwords.txt"
def text_preprocessing(text, tokenizer_wordcloud):
    # 불용어 목록을 GitHub에서 다운로드
    stopwords_url = "korean_stopwords.txt"
    stopwords = pd.read_csv(stopwords_url, header=None)[0].tolist()
    #stopwords += ['n', "''",'정말','너무','은','을','를','에','도','에로','같아','제','하는','이렇게','저렇게']  # 추가 불용어 정의

    # 한글과 영문 소문자를 제외한 모든 문자 제거
    text_cleaned = re.sub('[^가-힣a-z]', ' ', text)

    # 텍스트 토큰화
    tokens = tokenizer_wordcloud.morphs(text_cleaned)

    # 불용어 제거
    tokens_filtered = [token for token in tokens if token not in stopwords]

    return tokens_filtered

# Okt 형태소 분석기 인스턴스화
tokenizer_wordcloud = Okt()

# 각각의 감정별로 불용어 처리된 문장들의 단어 빈도를 계산
emotion_sentences = {'기쁨': [], '당황': [], '분노': [], '불안': [], '상처': [], '슬픔': []}
class_labels = ['기쁨', '당황', '분노', '불안', '상처', '슬픔']
word_frequencies = {emotion: Counter() for emotion in class_labels}

for emotion, sentences in emotion_sentences.items():
        for sentence in sentences:
                processed_text = text_preprocessing(sentence, tokenizer_wordcloud)
                word_frequencies[emotion].update(processed_text)

# 감정별 워드 클라우드 생성 및 시각화 (상위 20개 단어만 사용)
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # 워드 클라우드에 사용할 폰트 경로

for label, frequencies in word_frequencies.items():
    # 상위 20개 단어와 빈도수 추출
    top_words = frequencies.most_common(20)
    top_frequencies = {word: freq for word, freq in top_words}

    wordcloud = WordCloud(font_path=font_path, width=800, height=800, background_color='white').generate_from_frequencies(top_frequencies)

    print(label)
    plt.figure(figsize=(5, 5), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
