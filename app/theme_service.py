import openai
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time
from dotenv import load_dotenv
from PIL import Image
import os
import io
import json
import re
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import ChatCompletionsClient
from openai import AzureOpenAI

load_dotenv()

llama_token=os.getenv("llama_token")
llama_endpoint=os.getenv("llama_end")
llama_model=os.getenv("llama_model")

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

        screenshot_path = "screenshot.png"
        with open(screenshot_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")

        
        client = ChatCompletionsClient(
                endpoint=llama_endpoint,
                credential=AzureKeyCredential(llama_token)
            )
        
        messages = [
            {"role": "system", "content": "You are an expert in Tailwind CSS."},
            {"role": "user", "content": [{"type": "text", "text": "Extract the full @theme configuration for this screenshot with precise details. Capture all colors (including CTA buttons), typography, spacing, border-radius, and shadows accurately. Provide exact hex or RGB values to match the original design for an identical site recreation."},
            {"type": "image", "image": base64_image}]}
        ]
        
        response = client.complete(
            model=llama_model,  # Your deployment name in Azure
            messages=messages
        )
        return response.choices[0].message.content
    
    except Exception as e:
        driver.quit()
        return str(e), None
