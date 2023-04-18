from os import environ
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from dotenv import load_dotenv
load_dotenv()

LOGIN_URL = environ.get("LOGIN_URL")
PASSWORD = environ.get("PASSWORD")
EMAIL = environ.get("EMAIL")
FIRST_FREQUENCY = environ.get("FIRST_FREQUENCY")
SECOND_FREQUENCY = environ.get("SECOND_FREQUENCY")
THIRD_FREQUENCY = environ.get("THIRD_FREQUENCY")
FOURTH_FREQUENCY = environ.get("FOURTH_FREQUENCY")
DISH_FREQUENCY = environ.get("DISH_FREQUENCY")

links = [
    "",
]


def initialise_and_get_driver():
    # Set the path to the Brave browser binary
    brave_path = '/usr/bin/brave-browser'

    # Set the options for the Brave browser
    brave_options = webdriver.ChromeOptions()
    brave_options.binary_location = brave_path

    # Create a new instance of the Brave browser
    driver = webdriver.Chrome(options=brave_options)

    return driver


def login(driver):
    # Navigate to a website
    driver.get(LOGIN_URL)

    # login
    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")
    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    button = driver.find_element(By.NAME, "Sign in")
    button.click()


def open_link(link):
    driver.get(link)
    time.sleep(3)


def open_antenna_tool(driver):
    button = driver.find_element(By.XPATH, "//img[@alt='Hamburger icon']")
    wait = WebDriverWait(driver, 10)
    button = wait.until(expected_conditions.element_to_be_clickable(
        (By.XPATH, "//img[@alt='Hamburger icon']")))

    button.click()

    antennas_icon = driver.find_element(By.CLASS_NAME, "myx-icon-antenna")
    antennas_icon.click()


def add_up_to_4_patterns(antenna_div):
    add_pattern_btn = antenna_div.find_element(
        By.CSS_SELECTOR, ".hide-if-read-only.add-pattern")

    while len(antenna_div.find_elements(By.CSS_SELECTOR, "div[data-id]")) < 4:
        add_pattern_btn.click()
        # if i don't add timeout the program adds many divs
        # doesn't work with expected_condition either
        time.sleep(1)


def set_input_values(div_frequencies_wrapper, frequency, power):
    # change frequency value
    input_frequency = div_frequencies_wrapper.find_element(By.CSS_SELECTOR,
                                                           ".pattern-frequency")
    input_frequency.clear()
    input_frequency.send_keys(frequency)

    # change input power
    input_power = div_frequencies_wrapper.find_element(
        By.CSS_SELECTOR, ".pattern-power")
    input_power.clear()
    input_power.send_keys(power)


def find_and_add_input_values(antenna_div, isDish):
    div_frequencies_wrappers = antenna_div.find_elements(
        By.CSS_SELECTOR, "div[data-id]")
    for i, div_frequencies_wrapper in enumerate(div_frequencies_wrappers):
        if isDish:
            set_input_values(div_frequencies_wrapper, DISH_FREQUENCY, 0)
        else:
            if i == 0:
                set_input_values(div_frequencies_wrapper, FIRST_FREQUENCY, 80)
            elif i == 1:
                set_input_values(div_frequencies_wrapper,
                                 SECOND_FREQUENCY, 160)
            elif i == 2:
                set_input_values(div_frequencies_wrapper, THIRD_FREQUENCY, 160)
            elif i == 3:
                set_input_values(div_frequencies_wrapper,
                                 FOURTH_FREQUENCY, 160)


def iterate_antennas_wrappers_and_fill(driver):
    antennas_list = driver.find_element(By.ID, "antennas-list")
    antennas_divs = antennas_list.find_elements(By.CLASS_NAME, "antenna")

    for antenna_div in antennas_divs:
        isDish = False
        table_rows = antenna_div.find_elements(By.TAG_NAME, 'tr')
        for row in table_rows:
            if 'dish' in row.text or 'Diameter' in row.text:
                print('Dish antenna found')
                isDish = True
                find_and_add_input_values(
                    antenna_div=antenna_div, isDish=isDish)
                break
        if isDish:
            continue
        add_up_to_4_patterns(antenna_div=antenna_div)

        find_and_add_input_values(antenna_div=antenna_div, isDish=isDish)


driver = initialise_and_get_driver()

login(driver)

for link in links:
    time.sleep(1)
    open_link(link)

    open_antenna_tool(driver)

    iterate_antennas_wrappers_and_fill(driver)

driver.quit()
