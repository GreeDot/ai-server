from pydantic import BaseModel, Field
from typing import List, Dict

# 문장 하나 당 무슨 감정인지 응답 하나
class EmotionRequest(BaseModel):
    sentence: str

class EmotionResponse(BaseModel):
    emotion: str


# 문장 여러개 당 딕셔너리로 반환
class EmotionsRequest(BaseModel):
    sentences: List[str] = Field(..., example=["저는 오늘 기분이 좋아요", "이 소식을 듣고 매우 화가 났어요", '정말 당황스럽네요'])


class EmotionsResponse(BaseModel):
    emotions: Dict[str, List[str]]


# dict => wordcloud_path
class WordCloudRequest(BaseModel):
    emotions: Dict[str, List[str]] = Field(..., example={
    "기쁨": [
      "저는 오늘 기분이 좋아요"
    ],
    "당황": [
      "정말 당황스럽네요"
    ],
    "분노": [
      "이 소식을 듣고 매우 화가 났어요"
    ],
    "불안": [],
    "상처": [],
    "슬픔": []
  })

class WordCloudResponse(BaseModel):
    urls: Dict[str, str]

# gree_id => gpt_emotion_summary
class GptSummaryResponse(BaseModel):
    summary: str