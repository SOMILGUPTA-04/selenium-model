from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time

def capture_screenshot_and_extract_text(url, screenshot_path="screenshot.png"):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment if you want to run in headless mode
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)  # Wait for page load

        # Take Screenshot
        driver.save_screenshot(screenshot_path)
        print(f"✅ Screenshot saved at: {screenshot_path}")

        # Simulate "Ctrl + A" (Select All)
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        time.sleep(1)  # Wait for selection

        # Simulate "Ctrl + C" (Copy)
        action.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
        time.sleep(1)  # Wait for clipboard

        # Extract copied text from clipboard
        extracted_text = pyperclip.paste()
        print("✅ Extracted Text (Preview):\n", extracted_text[:4000])  # Print first 4000 chars

    finally:
        driver.quit()

    return extracted_text, screenshot_path


# Take URL input from the user
url = input("Enter the URL: ").strip()
text, screenshot = capture_screenshot_and_extract_text(url)
