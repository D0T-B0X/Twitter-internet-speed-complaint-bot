from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

REQUIRED_DOWN = 150.00
REQUIRED_UP = 150.00
executable_path = r"<path of chrome webdriver>"  # eg. my webdriver is stored in "C:\development\chromedriver.exe"
options = Options()
options.add_argument("load-extension=")
options.add_argument("--start-maximized")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 "
    "Safari/537.36"
)
service = Service()
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

driver.get("https://speedtest.net")
driver.switch_to.new_window('tab')
driver.get("https://www.twitter.com")


def twitter_login():
    wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div['
                                                  '3]/div[5]/a/div'))
    )
    sign_in = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div['
                                            '5]/a/div')
    sign_in.click()

    wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div['
                                                  '2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div['
                                                  '2]/div/input'))
    )
    username = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div['
                                             '2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
    username.send_keys("<Twitter username>")

    next_btn = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div['
                                             '2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
    next_btn.click()

    wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div['
                                                  '2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div['
                                                  '2]/div[1]/input'))
    )
    password = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div['
                                             '2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div['
                                             '1]/input')
    password.send_keys("<Twitter Password>")

    log_in = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div['
                                           '2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
    log_in.click()


twitter_login()


def speed_check():
    driver.switch_to.window(driver.window_handles[0])
    driver.get("https://www.speedtest.net")

    go = driver.find_element(By.CLASS_NAME, "start-text")
    go.click()
    sleep(45)

    try:
        cross = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div['
                                              '8]/div/div/div[2]/a')
        cross.click()
    except (
    selenium.common.exceptions.ElementNotInteractableException, selenium.common.exceptions.NoSuchElementException):
        pass

    down_speed = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div['
                                               '3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
    up_speed = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div['
                                             '3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
    speed_list = [float(down_speed), float(up_speed)]
    return speed_list


def twitter_post(down_speed: float, up_speed: float):
    driver.switch_to.window(driver.window_handles[1])

    wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div['
                                                  '3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]'))
    )
    message_post = driver.find_element(By.XPATH, '//html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div['
                                                 '3]/div/div[2]/div[1]/div/div/div/div[2]/div['
                                                 '1]/div/div/div/div/div/div/div/div/div/div/label/div['
                                                 '1]/div/div/div/div/div/div/div/div/div/div')
    message_post.send_keys(f"Hey @<Service Provider> why is my speed {down_speed} down/{up_speed} up when I pay for "
                           f"{REQUIRED_DOWN} down/ {REQUIRED_UP} up")

    post_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div['
                                             '3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/div['
                                             '3]/div/span/span')
    post_btn.click()


def run():
    speeds = speed_check()
    speed_down = speeds[0]
    speed_up = speeds[1]

    if speed_down < REQUIRED_DOWN or speed_up < REQUIRED_UP:
        twitter_post(speed_down, speed_up)


while True:
    run()
    sleep(60)

while True:
    run()
    sleep(60)
