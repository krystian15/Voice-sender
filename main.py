import time
import base64
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from voice_converter import ConvertSpeechToText


def decode_sting(string):
    base64_string = string
    base64_bytes = base64_string.encode('ascii')
    string_bytes = base64.b64decode(base64_bytes)
    return string_bytes.decode('ascii')


class VoiceMessageSender:
    settings: object
    user: object

    def __init__(self):

        with open('data.json') as file_settings:
            file_data = json.load(file_settings)
            self.settings = file_data.get('settings')
            self.user = file_data.get('user')

        converter = ConvertSpeechToText(self.settings.get('language'))

        self.message = converter.voice_recording()
        self.driver = webdriver.Chrome(self.settings.get('chrome_driver_path'))

        self.setup_page()
        self.login()
        self.select_your_girlfriend_text_input()
        self.driver.quit()

    def setup_page(self):
        self.driver.get(self.settings.get('page_url'))
        time.sleep(1)

    def login(self):
        """
        password
            Do not paste your not decode password! Use this online tool https://www.base64decode.org/ or other way
            to encode password
        """

        login_field = self.driver.find_element_by_xpath('//*[@id="email"]')
        password_field = self.driver.find_element_by_xpath('//*[@id="pass"]')
        submit_button = self.driver.find_element_by_xpath('//*[@id="loginbutton"]')

        email = self.user.get('email')
        phone = self.user.get('phone')

        if email:
            email_value = email
        else:
            email_value = phone

        login_field.send_keys(email_value)
        password_field.send_keys(decode_sting(self.user.get('password')))

        submit_button.click()
        time.sleep(2)

    def select_your_girlfriend_text_input(self):
        """
        user_target
            You can find it in dev tools browser,
            just search data-attr 'data-tooltip-content' and paste value to json user_target value
        """

        left_bar = self.driver.find_element_by_css_selector(
            f"div[data-tooltip-content='{self.settings.get('user_target')}']")

        left_bar.click()
        time.sleep(1)
        search_bar = self.driver.find_element_by_css_selector("div[contenteditable='true']")
        search_bar.click()

        search_bar.send_keys(self.message)
        search_bar.send_keys(Keys.ENTER)

    def send_like(self):
        like = self.driver.find_element_by_css_selector("a[data-testid='send_a_like_button']")
        like.click()


if __name__ == "__main__":
    VoiceMessageSender()
