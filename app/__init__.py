from fastapi import FastAPI, Form, Request
from dotenv import load_dotenv
import os
from app.theme_service import capture_screenshot_and_extract_css, generate_landing_page
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
                <button type="submit">Generate Landing Page</button>
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
    tailwind_css, base64_image = capture_screenshot_and_extract_css(url)
    html_content = generate_landing_page(tailwind_css, base64_image)
    
    output_path = "generated_page.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    
    return HTMLResponse(
        content=f'<html><body>{html_content}<br><a href="/download" download="generated_page.html"><button>Download HTML</button></a></body></html>',
        status_code=200
    )


@app.get("/download")
async def download_file():
    return FileResponse("generated_page.html", filename="generated_page.html")