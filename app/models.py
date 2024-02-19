from pydantic import BaseModel
from typing import List, Dict

# 문장 하나 당 무슨 감정인지 응답 하나
class EmotionRequest(BaseModel):
    sentence: str

class EmotionResponse(BaseModel):
    emotion: str


# 문장 여러개 당 딕셔너리로 반환
class EmotionsRequest(BaseModel):
    sentences: List[str]

class EmotionsResponse(BaseModel):
    emotions: Dict[str, List[str]]
