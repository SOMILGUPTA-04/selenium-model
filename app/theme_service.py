import openai
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time
from dotenv import load_dotenv
import os
import json

load_dotenv()

openai_api_key=os.getenv("openai_api_key")
openai_endpoint=os.getenv("openai_endpoint")
openai_version=os.getenv("openai_version")
openai_model_o4=os.getenv("openai_model_o4")

def capture_screenshot_and_extract_css(url, screenshot_path="screenshot.png"):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(5)
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, total_height)
        driver.save_screenshot(screenshot_path)
        driver.quit()

        with open(screenshot_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")
        
        client = openai.AzureOpenAI(
            api_key=openai_api_key,
            api_version=openai_version,
            azure_endpoint=openai_endpoint
        )
        
        messages = [
            {"role": "system", "content": "You are an expert in Tailwind CSS."},
            {"role": "user", "content": [{"type": "text", "text": " Please extract the Tailwind CSS @theme part in a very deatialed manner from the screenshot. So that it would be usefull in creating a site with identical elemnets. give only the theme part."},
            {"type": "image", "image": base64_image}]}
        ]
        response = client.chat.completions.create(
            model=openai_model_o4,
            messages=messages
        )
        return response.choices[0].message.content, base64_image
    
    except Exception as e:
        driver.quit()
        return str(e), None
