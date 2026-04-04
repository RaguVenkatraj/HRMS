import json
import os
import tempfile
import time
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from features.pages.login_page import LoginPage
from utils import config
from utils.config import parallel_run, Browser
from utils.env_config import env_config, mobile_config
from dotenv import load_dotenv


def before_all(context):
    print("Starting test execution")


def before_feature(context, feature):
    if not hasattr(context, 'driver'):
        print(f"Starting feature: {feature.name}")

        if config.Browser.lower() == "chrome":
            chrome_options = ChromeOptions()
            if os.environ.get("IN_DOCKER", "false").lower() == "true":
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--ignore-ssl-errors")
            chrome_options.add_argument("--allow-insecure-localhost")
            chrome_options.set_capability("acceptInsecureCerts", True)

            service = ChromeService(ChromeDriverManager().install())
            context.driver = webdriver.Chrome(service=service, options=chrome_options)

        elif config.Browser.lower() == "edge":
            edge_options = EdgeOptions()
            if os.environ.get("IN_DOCKER", "false").lower() == "true":
                edge_options.add_argument("--headless")
                edge_options.add_argument("--disable-gpu")
            edge_options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")
            service = EdgeService(EdgeChromiumDriverManager().install())
            context.driver = webdriver.Edge(service=service, options=edge_options)

        elif config.Browser.lower() == "firefox":
            firefox_options = FirefoxOptions()
            if os.environ.get("IN_DOCKER", "false").lower() == "true":
                firefox_options.add_argument("--headless")
            service = FirefoxService(GeckoDriverManager().install())
            context.driver = webdriver.Firefox(service=service, options=firefox_options)

        else:
            raise ValueError(f"Unsupported browser: {config.Browser}")

        config.run_type = "Jenkins - Docker" if os.environ.get("IN_DOCKER", "false").lower() == "true" else "Manual"
        if config.run_type == "Jenkins - Docker":
            context.driver.set_window_size(1920, 1080)
        else:
            context.driver.maximize_window()

            mobile_env = mobile_config()
            if mobile_env.get("is_enabled") and config.Browser.lower() == "chrome":
                mobile_emulation = {"deviceName": mobile_env["deviceName"]}
                chrome_options = ChromeOptions()
                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                context.driver.quit()
                service = ChromeService(ChromeDriverManager().install())
                context.driver = webdriver.Chrome(service=service, options=chrome_options)

        context.driver.implicitly_wait(10)

        load_dotenv()

        context.login_page = LoginPage(context.driver)


def after_feature(context, feature):
    if hasattr(context, 'driver'):
        context.driver.quit()
        del context.driver


def before_step(context, step):
    time.sleep(1)


def before_scenario(context, scenario):
    print(f"Starting scenario: {scenario.name}")


def after_scenario(context, scenario):
    if scenario.status == "failed":
        try:
            screenshot = context.driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Could not take screenshot: {e}")


def after_all(context):
    env_con = env_config()
    mobile_env = mobile_config()

    if config.run_type == "Jenkins - Docker":
        base_path = "/volume_data/allure-results"
    else:
        base_path = "allure-results"

    if parallel_run is True:
        if Browser.lower() == "chrome":
            path = os.path.join("allure-results-parallel", "chrome")
        elif Browser.lower() == "firefox":
            path = os.path.join("allure-results-parallel", "firefox")
        elif Browser.lower() == "edge":
            path = os.path.join("allure-results-parallel", "edge")
        else:
            path = base_path
    else:
        path = base_path

    os.makedirs(path, exist_ok=True)

    # Write environment.properties
    with open(f"{path}/environment.properties", "w") as f:
        if mobile_env.get("is_enabled"):
            f.write(f"Device={mobile_env['deviceName']}\n")
        else:
            f.write(f"Browser={config.Browser}\n")
        f.write(f"AppVersion={config.AppVersion}\n")
        f.write(f"Environment={env_con.get('ENVIRONMENT')}\n")
        f.write(f"URL={env_con.get('BASE_URL')}\n")

    # Write executor.json
    if mobile_env.get("is_enabled"):
        executor_info = {
            "name": "Mobile Emulation",
            "buildName": "Automated Test Run",
        }
    else:
        executor_info = {
            "name": config.run_type,
            "buildName": "Automated Test Run",
        }

    with open(f"{path}/executor.json", "w") as f:
        json.dump(executor_info, f, indent=2)

    print("Test execution finished.")
