from gen_ai import GenAI
from selenium import webdriver
from selenium.webdriver.common.by import By


def selenium_element():
    # Example usage
    driver = webdriver.Chrome()
    driver.get("")

    gen_ai = GenAI(driver)
    element = gen_ai.find_element_with_ai_healing(
        by=By.NAME,
        path="email",
        fallback_list=[(By.NAME, "user"), (By.XPATH, "//input[@placeholder='email']")],
        description="This is a email input field"
    )


# selenium_element()


def general_ask():
    # Example usage
    gen_ai = GenAI()
    prompt = "Hi, this is Ragu"
    answer = gen_ai.ask_ai(prompt)

    print(answer)


general_ask()
