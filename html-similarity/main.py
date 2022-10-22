import os
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


