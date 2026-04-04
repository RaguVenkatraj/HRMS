import google.generativeai as genai
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

try:
    from utils.config import AI_PROMPT, GEMINI_API_KEY, GEMINI_MODEL
except ModuleNotFoundError:
    from config import AI_PROMPT, GEMINI_API_KEY, GEMINI_MODEL


class GenAI:

    def __init__(self, driver=WebDriver):
        self.driver = driver
        self.api_key = GEMINI_API_KEY
        self.model_name = GEMINI_MODEL
        genai.configure(api_key=self.api_key)

    def get_prompt(self, description, by, path, snippet):
        return AI_PROMPT.format(
            description=description,
            by=by,
            path=path,
            snippet=snippet
        )

    def find_element_with_ai_healing(self, by, path, fallback_list=None, description=None):
        # Primary locator
        try:
            element = self.driver.find_element(by, path)
            print(f"[✓] Found element: {by}={path}")
            return element
        except NoSuchElementException:
            print(f"[!] Primary locator failed: {by}={path}")

        # Fallback locators
        if fallback_list:
            for fb_by, fb_path in fallback_list:
                try:
                    element = self.driver.find_element(fb_by, fb_path)
                    print(f"[✓] Found fallback: {fb_by}={fb_path}")
                    return element
                except NoSuchElementException:
                    continue
            print("[!] All fallback locators failed.")

        # AI healing
        try:
            body = self.driver.find_element(By.TAG_NAME, "body")
            html = body.get_attribute("outerHTML")
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style", "svg", "noscript", "img"]):
                tag.decompose()
            snippet = soup.prettify()[:3000]

            prompt = self.get_prompt(description, by, path, snippet)

            print(f"The prompt: {prompt}")
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            ai_xpath = response.text.strip().strip('`').replace("xpath=", "")
            print(f"[AI] Trying XPath: {ai_xpath}")

            self.driver.find_element(By.XPATH, ai_xpath)
            print(f"[✓] Found element with AI suggestion | {ai_xpath} ")
            return ai_xpath

        except Exception as e:
            print(f"[X] AI healing failed: {e}")
            raise NoSuchElementException("Element not found by any locator.")

    def ai_self_heal(self, by, path, description=None):
        try:
            body = self.driver.find_element(By.TAG_NAME, "body")
            html = body.get_attribute("outerHTML")
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style", "svg", "noscript", "img"]):
                tag.decompose()
            snippet = soup.prettify()[:3000]

            prompt = self.get_prompt(description, by, path, snippet)

            print(f"The prompt: {prompt}")
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            ai_xpath = response.text.strip().strip('`').replace("xpath=", "")
            print(f"[AI] Trying XPath: {ai_xpath}")

            self.driver.find_element(By.XPATH, ai_xpath)
            print(f"[✓] Found element with AI suggestion | {ai_xpath} ")

            return ai_xpath

        except Exception as e:
            print(f"[X] AI healing failed: {e}")
            raise NoSuchElementException("Element not found by any locator.")

    def ask_ai(self, prompt):
        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(prompt)

        return f"AI says: {response.text}"
