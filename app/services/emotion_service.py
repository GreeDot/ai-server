from services.emotion_model import predict_emotion
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def predict_emotion_from_service(sentence, max_len=64):
    return predict_emotion(sentence, max_len)

def create_emotion_wordcloud(emotion_sentences: list):
    text = " ".join(emotion_sentences)
    wordcloud = WordCloud(font_path='/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf', background_color="white").generate(text)
    
    # 이미지 파일로 저장
    wordcloud.to_file("/tmp/emotion_wordcloud.png")
