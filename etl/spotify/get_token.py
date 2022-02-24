
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from utils.misc import httpx_request
from airflow.models import Variable

def token_web(LIMIT):
    browser = webdriver.Chrome(ChromeDriverManager().install())

    browser.get("https://developer.spotify.com/console/get-recently-played/?limit=10&after=&before=")
    time.sleep(3)
    get_token = browser.find_element_by_xpath("/html/body/div[1]/div/div/main/article/div[2]/div/div/form/div[3]/div/span/button")
    get_token.click()
    time.sleep(3)
    user_click = browser.find_element_by_xpath("/html/body/div[1]/div/div/main/article/div[2]/div/div/div[1]/div/div/div[2]/form/div[2]/div/div[17]/div/label/span")
    user_click.click()
    time.sleep(2)
    request_token = browser.find_element_by_xpath("/html/body/div[1]/div/div/main/article/div[2]/div/div/div[1]/div/div/div[2]/form/input")
    request_token.click()
    time.sleep(5)
    facebook_button = browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/button[1]")
    facebook_button.click()
    time.sleep(3)
    facebook_username = browser.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[1]/input")
    facebook_username.send_keys(Variable.get("FB_LOGIN"))
    time.sleep(1)
    facebook_password = browser.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[2]/input")
    facebook_password.send_keys(Variable.get("FB_PASSWORD"))
    time.sleep(2)
    facebook_sign_in = browser.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/button")
    facebook_sign_in.click()
    time.sleep(3)
    String_text = browser.find_element_by_id("oauth-input")
    TOKEN = String_text.get_attribute("value")
    browser.close()

    url = 'https://api.spotify.com/v1/me/player/recently-played?limit={}'.format(LIMIT)
    header = {'Authorization': f'Bearer {TOKEN}'}
    res = httpx_request(url, header)
    return res

if __name__ == '__main__':
    token_web()