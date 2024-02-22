import os
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import Field
from services.gpt_summary_service import DialogueService
from services.wordcloud_service import generate_and_save_wordclouds, sentences_to_wordcloud, text_preprocessing, upload_file_azure
from models import EmotionRequest, EmotionResponse, EmotionsRequest, EmotionsResponse, GptSummaryResponse, WordCloudRequest, WordCloudResponse
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

# API 엔드포인트 정의
@router.post("/emotion-summary/{gree_id}", response_model=GptSummaryResponse)
async def emotion_summary_api(gree_id: int):
    # 실제 구현에서는 이 값들을 환경 변수나 설정 파일에서 불러오는 것이 좋습니다.
    # api_url = f"http://20.196.198.166:8000/api/v1/log/gree/{gree_id}"
    api_url = f"http://localhost:8000/api/v1/log/gree/{gree_id}"
    chatgpt_api_url = "https://api.openai.com/v1/chat/completions"
    chatgpt_api_key = os.getenv('OPENAI_API_KEY')  # 실제 사용 시 API 키로 교체

    dialogues = DialogueService.fetch_dialogue_logs(api_url)
    if dialogues:
        summary = DialogueService.summarize_dialogue_for_parents(dialogues, chatgpt_api_url, chatgpt_api_key)
        return GptSummaryResponse(summary=summary)
    else:
        raise HTTPException(status_code=404, detail="대화 로그를 가져올 수 없습니다.")