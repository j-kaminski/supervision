import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import math
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from collections import Counter


class HTMLSimilarity:
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'}

    def __init__(self):
        self.driver = self._create_driver()

    def _create_driver(self):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        return driver
        
    def get_soup_text(self, dir_path, file_name):
        html_text = None
        with open(os.path.join(dir_path, file_name), 'r') as f:
            html_text = BeautifulSoup(f.read(), 'html.parser').get_text()
        return html_text

    def filtered_text(self, text):
        list_words = re.split(r'\W', text)
        text = [word.lower() for word in list_words if len(word) > 1 and not word.isnumeric()]
        return text

    def get_cosine(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def download_legit_domains(self):
        dir_path = os.path.join(os.path.dirname(__file__), 'html_legit_domain_pages')

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open('domains.txt', 'r') as f:
            urls = f.readlines()
            for url in urls:
                self.download_html(dir_path, url)
    
    def download_html(self, dir_path, url):
        url_parsed = urlparse(url).netloc
        if not os.path.exists(os.path.join(dir_path, f'{url_parsed}.html')): 
            with open(os.path.join(dir_path, f'{url_parsed}.html'), 'wb') as f:
                    print('download', url_parsed)
                    self.driver.get(url)
                    content = self.driver.page_source
                    # r = requests.get(url, headers=self.HEADERS)
                    f.write(content.encode()) 
    
    def make_tokenizer(self):
        pass

current_dir_path = os.path.dirname(__file__)

h = HTMLSimilarity() 
# scam = 'https://ca24credlt-agrlcole.top/offers.php'
# path_to_scam = os.path.join(current_dir_path, urlparse(scam).netloc)
# h.download_html(current_dir_path, scam)
scam_html = 'millen.html'

legit_dir = os.path.join(current_dir_path, 'html_legit_domain_pages')
legit_html_list = [path for path in os.listdir(legit_dir)]


results = []
for html_file in legit_html_list:
    legit_soup = h.get_soup_text(legit_dir, html_file)
    scam_soup = h.get_soup_text(current_dir_path, scam_html)

    filtered_text_legit = h.filtered_text(legit_soup)
    filtered_text_scam = h.filtered_text(scam_soup)
    result = h.get_cosine(Counter(filtered_text_legit), Counter(filtered_text_scam))
    print(result, html_file)
    results.append((result, html_file))

    
# print(max(results))

    


# legit_dir = os.path.join(os.path.dirname(__file__))
# scam_dir = os.path.join(os.path.dirname(__file__), 'scam_html')
# h.download_html(scam_dir, scam)
# scam stronka pobrać
# 
# current_dir = os.path.dirname(__file__)
# agricole_dir = os.path.join(current_dir, 'agricole')
# real_html_text = get_soup_text(current_dir, 'real_agricole.html') 
# real_html_text = get_soup_text(current_dir, 'pekao.html') 
# real = formatting_text(real_html_text)
# fake_html_text = get_soup_text(agricole_dir, 'fake_agricole.html') 
# fake = formatting_text(fake_html_text)
# x = get_cosine(Counter(real), Counter(fake))
# print(x)
# small_length = min(len(real), len(fake))
# for i in range(small_length):
#     print(real[i], fake[i])
import re
from bs4 import BeautifulSoup


current_dir = os.path.join(os.path.dirname(__file__), 'agricole')

def get_soup_text(dir_path, file_name):
    html_text = None
    with open(os.path.join(dir_path, file_name), 'r') as f:
        html_text = BeautifulSoup(f.read(), 'html.parser').get_text()
    return html_text


def formatting_text(text):
    list_words = re.split(r'\W', text)
    text = [word.lower() for word in list_words if len(word) > 1 and not word.isnumeric()]
    return text

real_html_text = get_soup_text(current_dir, 'real_agricole.html') 
real = formatting_text(real_html_text)

print(real)
fake_html_text = get_soup_text(current_dir, 'fake_agricole.html') 
fake = formatting_text(fake_html_text)
print(fake)

