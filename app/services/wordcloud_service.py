from typing import Dict, List
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Okt
import pandas as pd
import re
import os
import uuid
from fastapi import HTTPException
from azure.storage.blob import BlobServiceClient, ContentSettings

from models import WordCloudRequest, WordCloudResponse

def upload_file_azure(file_path: str) -> str:
    try:
        container_name = "greefile"
        AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY")
        if not AZURE_ACCOUNT_KEY:
            raise HTTPException(status_code=500, detail="Azure account key is not set in environment variables.")

        connection_string = f"DefaultEndpointsProtocol=https;AccountName=greedotstorage;AccountKey={AZURE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # 파일 이름 추출 및 고유한 파일 이름 생성
        file_name = os.path.basename(file_path)
        unique_file_name = f"wordcloud/{uuid.uuid4()}_{file_name}"

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=unique_file_name)

        # 파일 형식에 따라 content_type 설정
        content_type = 'application/octet-stream'  # 기본 값
        if file_name.lower().endswith('.png'):
            content_type = 'image/png'
        elif file_name.lower().endswith('.gif'):
            content_type = 'image/gif'
        elif file_name.lower().endswith('.jpg') or file_name.lower().endswith('.jpeg'):
            content_type = 'image/jpeg'
        elif file_name.lower().endswith('.mp3'):
            content_type = 'audio/mpeg'

        # 파일 업로드
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True, content_settings=ContentSettings(content_type=content_type))

        # 업로드된 파일의 URL 반환
        return blob_client.url
    except Exception as e:
        print(f"An error occurred while uploading the file to Azure: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file to Azure: {e}")

def update_stopwords(new_stopwords, stopwords_file = "services/assets/korean_stopwords.txt"):
    # "korean_stopwords.txt" 파일에서 기존 불용어 리스트 읽기
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        existing_stopwords = file.read().splitlines()
    # 기존 불용어 리스트에 새로운 불용어 추가 및 중복 제거
    updated_stopwords = list(set(existing_stopwords + new_stopwords))
    # 변경된 불용어 리스트를 파일에 저장
    with open(stopwords_file, 'w', encoding='utf-8') as file:
        for stopword in updated_stopwords:
            file.write(stopword + '\n')

def text_preprocessing(text, tokenizer_wordcloud = Okt(), stopwords_file = "services/assets/korean_stopwords.txt"):
    stopwords = pd.read_csv(stopwords_file, header=None)[0].tolist()
    text_cleaned = re.sub('[^가-힣a-z]', ' ', text)
    tokens = tokenizer_wordcloud.morphs(text_cleaned)
    tokens_filtered = [token for token in tokens if token not in stopwords]
    return tokens_filtered

def generate_and_save_wordclouds(word_frequencies, font_path, output_dir) -> list:
    saved_files = []
    for label, frequencies in word_frequencies.items():
        top_frequencies = {word: freq for word, freq in frequencies.most_common(20)}
        if not top_frequencies:
            top_frequencies = {"": 1}  # 빈 워드 클라우드 처리
        wordcloud = WordCloud(font_path=font_path, width=800, height=800, background_color='white').generate_from_frequencies(top_frequencies)
        plt.figure(figsize=(5, 5), facecolor=None)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)
        # PNG 파일로 저장
        file_path = f'{output_dir}/{label}.png'
        plt.savefig(file_path)
        plt.close()
        saved_files.append(file_path)
    return saved_files

# sentences를 받아 dict로 azure의 wordcloud url을 받음.
def sentences_to_wordcloud(wordClouRequest: WordCloudRequest) -> WordCloudResponse:
    new_stopwords = ['하지', '얘기', '정도', '라', '스러워요', '스럽네', '텐데', '싶어서', '보면', '전혀', '곳', '나를', '않고', '팀', '자리', '없어서', '없는', '하니까', '같은']
    emotion_sentences = wordClouRequest.emotions
    word_frequencies = {emotion: Counter() for emotion in emotion_sentences}

    for emotion, sentences in emotion_sentences.items():
        for sentence in sentences:
            processed_text = text_preprocessing(sentence)
            word_frequencies[emotion].update(processed_text)

    # 워드 클라우드 생성 및 PNG 파일로 저장
    font_path = 'services/assets/NanumGothic.ttf'
    output_dir = 'tmp/wordcloud_images'  # 워드 클라우드 이미지를 저장할 디렉토리
    saved_files = generate_and_save_wordclouds(word_frequencies, font_path, output_dir)

    # Azure에 업로드하고 URL 매핑
    emotion_to_url = {}
    for file_path in saved_files:
        emotion = file_path.split('/')[-1].split('.')[0]  # 파일 경로에서 감정 추출
        uploaded_url = upload_file_azure(file_path)
        emotion_to_url[emotion] = uploaded_url

    return emotion_to_url


if __name__ == '__main__':
    emotion_sentences = {'기쁨': ['정말 기뻐'], '당황': ['당황스러워'], '분노': [], '불안': [], '상처': [], '슬픔': []}
    print(sentences_to_wordcloud(emotion_sentences))