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

# def capture_screenshot_and_extract_text(url, screenshot_path="screenshot.png"):
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # Uncomment if you want to run in headless mode
#     chrome_options.add_argument("--disable-gpu")  

#     driver = webdriver.Chrome(options=chrome_options)

#     try:
#         driver.get(url)
#         time.sleep(5)  # Wait for page load

#         # Get the total height of the page
#         total_height = driver.execute_script("return document.body.scrollHeight")
#         driver.set_window_size(1920, total_height)

#         # Take Screenshot
#         driver.save_screenshot(screenshot_path)
#         print(f"✅ Screenshot saved at: {screenshot_path}")

#         def encode_image(image_path):
#             """Convert an image to a base64 string for API request"""
#             with open(image_path, "rb") as img_file:
#                 return base64.b64encode(img_file.read()).decode("utf-8")

#         def analyze_screenshot_with_gpt4o(image_path):
#             base64_image = encode_image(image_path)
#             messages=[
#                 {"role": "system", "content": "You are a Tailwind CSS expert who extracts UI styles from images."},
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": "Analyze this screenshot and generate a Tailwind CSS theme that matches the styles. Only give me the @theme part of the css file and nothing else. Don't add ```css or ``` at the start or end."},
#                         {"type": "image", "image": base64_image}
#                     ]
#                 }
#             ]
#             # for production using gpt4o
#             client = openai.AzureOpenAI(
#                 api_key=f"{openai_api_key}",
#                 api_version=openai_version,
#                 azure_endpoint=f"{openai_endpoint}"
#             )
#             response = client.chat.completions.create(
#                 model=openai_model_o4,  # Your deployment name in Azure
#                 messages=messages
#             )
#             return response.choices[0].message.content

#         # Analyze the screenshot with GPT-4
#         analysis_result = analyze_screenshot_with_gpt4o(screenshot_path)
#         return analysis_result

#     finally:
#         driver.quit()


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
            {"role": "system", "content": "Extract Tailwind CSS theme from UI screenshot."},
            {"role": "user", "content": [{"type": "text", "text": "Extract Tailwind CSS @theme part."},
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


def generate_landing_page(tailwind_css, base64_image):
    client = openai.AzureOpenAI(
        api_key=openai_api_key,
        api_version=openai_version,
        azure_endpoint=openai_endpoint
    )
    messages = [
        {"role": "system", "content": "You are an expert in generating landing pages from Tailwind CSS themes."},
        {"role": "user", "content": f"Give a modern landing page that uses direct colors and similar stylng from the following Tailwind CSS theme:{json.dumps(tailwind_css)}. Don't add ```html or ``` at the start or end."}
    ]
    response = client.chat.completions.create(
        model=openai_model_o4,
        messages=messages
    )
    return response.choices[0].message.content

