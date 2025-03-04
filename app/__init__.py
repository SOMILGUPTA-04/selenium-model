from fastapi import FastAPI, Form, Request
from dotenv import load_dotenv
import os
from app.theme_service import capture_screenshot_and_extract_css
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def serve_form():
    return """
    <html>
        <body>
            <form action="/process" method="post">
                <label>Enter URL:</label>
                <input type="text" name="url" required>
                <button type="submit">Extract theme</button>
            </form>
        </body>
    </html>
    """


# @app.get("/theme")
# async def read_item(url: str):
#     result = capture_screenshot_and_extract_css(url)
#     return {"analysis": result}

@app.post("/process")
async def process_url(url: str = Form(...)):
    tailwind_css = capture_screenshot_and_extract_css(url)
    return {
        "tailwind_css": tailwind_css,
    }