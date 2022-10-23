from selenium import webdriver
from urllib.parse import urlparse
from selenium.webdriver.firefox.options import Options
from time import sleep
import os


class ScreenShoter():
    def __init__(self):
        self.driver = self._create_driver()
        self.screenshots_dir = 'screenshots'
        self.script_path = os.path.dirname(__file__)
        self.screenshots_path = os.path.join(self.script_path, self.screenshots_dir)
        if not os.path.exists(self.screenshots_path):
            os.makedirs(self.screenshots_path )

    def _create_driver(self):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        return driver

    def take_screenshot(self, url):
        print(url)
        self.driver.get(url)
        parsed_url = urlparse(url)
        ss_path = os.path.join(self.screenshots_path, parsed_url.netloc)
        os.makedirs(ss_path)
        self.driver.get_screenshot_as_file(os.path.join(ss_path, "screenshot.png"))
   
    def save_ss_legit_domains(self):
        domains_file = os.path.join(self.script_path, 'domains.txt')
        with open(domains_file, 'r') as f:
            legit_urls = f.readlines()
            for legit_url in legit_urls:
                self.take_screenshot(legit_url)
        self.driver.exit()




ss = ScreenShoter()
ss.save_ss_legit_domains()
