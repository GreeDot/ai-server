from fastapi import APIRouter, HTTPException
from models import EmotionRequest, EmotionResponse, EmotionsRequest, EmotionsResponse
from services.emotion_service import create_emotion_wordcloud, predict_emotion_from_service

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

@router.post("/create-emotion-wordcloud")
async def create_emotion_wordcloud_api(request: EmotionsRequest):
    try:
        emotion_sentences = sum(request.emotions.values(), [])  # 모든 감정 문장을 하나의 리스트로 합침
        create_emotion_wordcloud(emotion_sentences)
        return File("/tmp/emotion_wordcloud.png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))