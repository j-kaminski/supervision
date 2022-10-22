import os
import math
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from collections import Counter


class HTMLSimilarity:
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'}

    def __init__(self):
        pass
        
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

    
    def download_html(self, url):
        url_parsed = urlparse(url).netloc
        with open(f'{url_parsed}.html', 'wb') as f:
            r = requests.get(url, headers=self.HEADERS)
            f.write(r.content) 
    
    def make_tokenizer(self):
        pass
    
# scam stronka pobrać
# 
# h = HTMLSimilarity()
# h.download_html('https://stackoverflow.com/questions/70414902/why-is-the-python-module-requests-downloading-the-html-page-instead-of-a-file')
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
