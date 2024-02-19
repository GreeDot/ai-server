from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import Field
from services.wordcloud_service import generate_and_save_wordclouds, sentences_to_wordcloud, text_preprocessing, upload_file_azure
from models import EmotionRequest, EmotionResponse, EmotionsRequest, EmotionsResponse, WordCloudRequest, WordCloudResponse
from services.emotion_service import create_emotion_wordcloud, predict_emotion_from_service
from collections import Counter

router = APIRouter()

@router.post("/predict-emotion", response_model=EmotionResponse)
async def predict_emotion_api(request: EmotionRequest):
    try:
        predicted_emotion = predict_emotion_from_service(request.sentence)
        return EmotionResponse(emotion=predicted_emotion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict-emotions", response_model=EmotionsResponse)
async def predict_emotions_api(request: EmotionsRequest):
    emotions_dict = {'기쁨': [], '당황': [], '분노': [], '불안': [], '상처': [], '슬픔': []}
    try:
        for sentence in request.sentences:
            predicted_emotion = predict_emotion_from_service(sentence)
            if predicted_emotion in emotions_dict:
                emotions_dict[predicted_emotion].append(sentence)
        return EmotionsResponse(emotions=emotions_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 워드 클라우드 생성 및 Azure 업로드 함수
@router.post("/make-wordcloud")
async def upload_emotion(request: WordCloudRequest):
    try:
        wordcloud_url = sentences_to_wordcloud(request)
        return WordCloudResponse(urls=wordcloud_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))