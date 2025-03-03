from fastapi import FastAPI
from dotenv import load_dotenv
import os
from app.theme_service import capture_screenshot_and_extract_text

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Hello World"}

@app.get("/theme")
async def read_item(url: str):
    result = capture_screenshot_and_extract_text(url)
    return {"analysis": result}
