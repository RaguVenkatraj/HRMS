import json
import time
import re
import random
import string
import allure
from PIL import Image
import io
from datetime import datetime
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from utils import config
from utils.env_config import env_config


def __init__(self, driver: WebDriver):
    self.driver = driver
    # self.driver = webdriver.Chrome


def get_text(self, LOCATOR):
    try:
        text = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, LOCATOR))).text
        return text
    except Exception:
        print(f"Element not found - {LOCATOR}")


def get_multiple_text(self, LOCATOR):
    extracted_data_list = []
    extracted_data = self.driver.find_elements(By.XPATH, LOCATOR)
    for i in extracted_data:
        extracted_data_list.append(i.text)
    return extracted_data_list


def wait_till_visibility_of_element_located(self, LOCATOR):
    try:
        # scrollto = self.driver.find_element(By.XPATH, LOCATOR)
        # self.driver.execute_script("arguments[0].scrollIntoView(true);", scrollto)
        WebDriverWait(self.driver, 10, poll_frequency=2).until(EC.visibility_of_element_located((By.XPATH, LOCATOR)))
    except Exception:
        print(f"Element not found - {LOCATOR}")
        raise AssertionError(f"Element not found - {LOCATOR}")


def wait_till_element_to_be_clickable_and_then_click(self, LOCATOR, retries=2, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            WebDriverWait(self.driver, 20, poll_frequency=2).until(
                EC.element_to_be_clickable((By.XPATH, LOCATOR))).click()
            return

        except Exception:
            print(f"[Retry {attempt + 1}] Element not clickable yet. Retrying in {delay} seconds... | {LOCATOR}")
            time.sleep(delay)
            attempt += 1

    if attempt == retries:
        raise Exception(f"Element not found - {LOCATOR}")


def wait_till_element_to_be_clickable(self, LOCATOR):
    try:
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, LOCATOR)))
    except AssertionError:
        print(f"Element not clickable | {LOCATOR}")


def scroll_to_element(self, LOCATOR):
    scroll = self.driver.find_element(By.XPATH, LOCATOR)
    # self.driver.execute_script("arguments[0].scrollIntoView(true);", scroll)
    self.driver.execute_script("""
        arguments[0].scrollIntoView({
            behavior: 'smooth',
            block: 'center',
            inline: 'nearest'
        });
    """, scroll)


def scroll_table(self, locator_class, scroll_to=None):
    scrollable_div = self.driver.find_element(By.CLASS_NAME, locator_class)
    if scroll_to == "top":
        self.driver.execute_script("arguments[0].scrollTop = 0;", scrollable_div)
    if scroll_to == "bottom":
        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_div)


def click_based_on_axis(self, x, y):
    actions = ActionChains(self.driver)
    actions.move_by_offset(x, y).click().perform()


def click_based_on_actionchains(self, LOCATOR):
    time.sleep(2)
    element = self.driver.find_element(By.XPATH, LOCATOR)
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click().perform()


def date_picker_date_selection(self, LOCATOR, DATE):
    wait_till_element_to_be_clickable(self, LOCATOR)
    date_input = self.driver.find_element(By.XPATH, LOCATOR)
    self.driver.execute_script("""
              const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
              const input = arguments[0];
              const value = arguments[1];
              nativeInputValueSetter.call(input, value);
              input.dispatchEvent(new Event('input', { bubbles: true }));
              input.dispatchEvent(new Event('change', { bubbles: true }));
            """, date_input, DATE)


def allure_attach_data(data, FileName="Data"):
    allure.attach(
        body=str(data),
        name=FileName,
        attachment_type=allure.attachment_type.TEXT
    )


def allure_attach_json(data, FileName="Data"):
    allure.attach(
        body=json.dumps(data, indent=2),
        name=FileName,
        attachment_type=allure.attachment_type.JSON
    )


def allure_attach_screenshot(self, locator=None, screenshot_type=None):
    if screenshot_type == "element":
        screenshot = self.driver.find_element(By.XPATH, locator).screenshot_as_png
        allure.attach(
            screenshot,
            name="Element Screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    else:
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(
            screenshot,
            name="Screenshot",
            attachment_type=allure.attachment_type.PNG
        )


def allure_attach_fullpage_screenshot(self, scroll_pause_time=2):
    total_width = self.driver.execute_script("return document.body.scrollWidth")
    total_height = self.driver.execute_script("return document.body.scrollHeight")
    viewport_height = self.driver.execute_script("return window.innerHeight")
    viewport_width = self.driver.execute_script("return window.innerWidth")

    rectangles = []
    for y in range(0, total_height, viewport_height):
        height = min(viewport_height, total_height - y)
        rectangles.append((0, y, viewport_width, height))

    stitched_image = Image.new('RGB', (total_width, total_height))

    for rect in rectangles:
        x, y, width, height = rect
        self.driver.execute_script(f"window.scrollTo({x}, {y});")
        time.sleep(scroll_pause_time)
        png = self.driver.get_screenshot_as_png()
        screenshot = Image.open(io.BytesIO(png))
        crop_box = (0, screenshot.height - height, width, screenshot.height)
        viewport_screenshot = screenshot.crop(crop_box)
        stitched_image.paste(viewport_screenshot, (x, y))
    img_byte_arr = io.BytesIO()
    stitched_image.save(img_byte_arr, format='PNG')

    allure.attach(
        img_byte_arr.getvalue(),
        name="FullPage Screenshot",
        attachment_type=allure.attachment_type.PNG
    )


def add_call_deatils(DATA, Type=None):
    try:
        file_path = "data/actual_category_and_question_list.py"
        with open(file_path, "r+", encoding="utf-8") as f:
            content = f.read()
            if Type == "clean_needed":
                cleaned = [re.sub(r'^Q\d+:\s*', '', q.strip()) for group in DATA for q in group]
                if "questions_list" in content:
                    content = re.sub(
                        r"questions_list\s*=\s*\[.*?\](\n)?",
                        f"questions_list = {cleaned}\n",
                        content,
                        flags=re.DOTALL
                    )
                else:
                    content += f"\nquestions_list = {cleaned}\n"
            elif Type == "no_clean_needed":
                if "category_list" in content:
                    content = re.sub(
                        r"category_list\s*=\s*\[.*?\](\n)?",
                        f"category_list = {DATA}\n",
                        content,
                        flags=re.DOTALL
                    )
                else:
                    content += f"\ncategory_list = {DATA}\n"
            f.seek(0)
            f.write(content)
            f.truncate()

            return True

    except Exception:
        print("Issue encountered when writing the file.")
        return False


def date_and_time():
    now = datetime.now()
    date_time = now.strftime("%d/%m/%y - %H:%M:%S")

    return date_time


def date():
    now = datetime.now()
    current_date = now.strftime("%m/%d/%Y")

    return current_date


def get_attr_src(self, locator):
    images = self.driver.find_elements(By.XPATH, locator)
    image_sources = [img.get_attribute("src") for img in images]

    return image_sources


def get_attr_value(self, locator):
    element = self.driver.find_elements(By.XPATH, locator)
    element_attr = [ele.get_attribute("value") for ele in element]

    return element_attr


def ramdom_string_int():
    random_str_int = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))

    return random_str_int


def select_dropdown(self, css_locator, value):
    dropdown = self.driver.find_element(By.CSS_SELECTOR, css_locator)
    select = Select(dropdown)
    select.select_by_value(value)


def generate_tempmail(self):
    EMAIL = "//input[@placeholder='Name']"
    DOMAIN = "//button[@id='domain']"

    self.driver.switch_to.new_window('tab')
    self.driver.get("https://tempmail.plus/")
    wait_till_visibility_of_element_located(self, EMAIL)

    generated_email = f"real_email.autotest.{ramdom_string_int()}"
    self.driver.find_element(By.XPATH, EMAIL).clear()
    self.driver.find_element(By.XPATH, EMAIL).send_keys(generated_email + Keys.ENTER, Keys.ENTER)
    domain_name = get_text(self, DOMAIN)
    self.driver.switch_to.window(self.driver.window_handles[0])

    print(generated_email + domain_name)

    return generated_email + domain_name
