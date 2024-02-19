from fastapi import FastAPI
from routers import emotion_router
import uvicorn

app = FastAPI()

# 라우터 추가
app.include_router(emotion_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, log_level="debug")
