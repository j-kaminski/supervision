from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import cv2
import numpy as np

def website_ss(url):
    options = Options()
    options.headless = True
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    img = driver.get_screenshot_as_png()
    nparr = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    driver.close()
    return img