from json import loads
from pathlib import Path
from urllib.parse import urlparse

from requests import get
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Tokenizer:
    @staticmethod
    def filter_tokenize_hostname(hostname):
        if not hostname:
            return None

        skip_tokens = {
            'www',
        }

        tokens = set(hostname.split('.'))

        for match in tokens.intersection(skip_tokens):
            tokens.remove(match)
        tokens = list(filter(None, tokens))
        return ' '.join(tokens) or None

    @staticmethod
    def filter_tokenize_path(path):
        if not path:
            return None

        tokens = list(filter(None, set(path.split('/'))))
        return tokens or None

    @staticmethod
    def tokenize_url(url):
        if not url:
            return None

        fixed_url = url
        if '://' not in fixed_url:
            fixed_url = f'http://{url}'

        parsed_url = urlparse(fixed_url)

        tokenized = {
            url: {
                'scheme': parsed_url.scheme or None,
                'tokens': Tokenizer.filter_tokenize_hostname(parsed_url.hostname),
                'path': Tokenizer.filter_tokenize_path(parsed_url.path)
            }
        }
        return tokenized


class Extractor:
    @staticmethod
    def extract_links_from_samples(path):
        links = []
        data_dir = Path(path).glob('**/*.json')
        for file in data_dir:
            json_content = loads(file.read_text())
            url = json_content['url']
            tokenized = Tokenizer.tokenize_url(url)
            links.append(tokenized)
        return links

    @staticmethod
    def extract_links_from_file(path):
        result = {}
        links = Path(path).read_text().split()
        for item in map(Tokenizer.tokenize_url, links):
            result.update(item)
        return result

    @staticmethod
    def extract_links_from_url(path):
        result = {}
        links = get(path).text.split()
        for item in map(Tokenizer.tokenize_url, links):
            result.update(item)
        return result


class Similarity:
    vectorizer = TfidfVectorizer()

    def __init__(self, legit_links, threshold=0.7):
        self.legit_links = legit_links
        self.threshold = threshold
        self.legit_tokens = None
        self.tfidf_matrix = None
        self.tfidf_vectorizer = None
        self.prepare_vectorizer()

    def get_best_match(self, url):
        link = Tokenizer.tokenize_url(url)
        query = link[url]['tokens']
        # TODO: dodanie to co paweł powiedział czyli ostatnie dwa tokeny najważniejsze (lub 3).
        query_tfidf = self.tfidf_vectorizer.transform([query])
        cos_sim = cosine_similarity(query_tfidf, self.tfidf_matrix)
        results = cos_sim[0:1].flatten()[1:]
        best_result_idx = results.argmax()
        score = results[best_result_idx]
        link = self.get_link_by_idx(best_result_idx + 1)
        return self.apply_threshold(link, score)

    def prepare_vectorizer(self):
        self.tfidf_vectorizer = TfidfVectorizer(analyzer='char')
        self.legit_tokens = [link['tokens'] for link in self.legit_links.values()]
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.legit_tokens)

    def get_link_by_idx(self, idx):
        token = self.legit_tokens[idx]
        return self.get_link_by_token(token)

    def get_link_by_token(self, token):
        for k, v in self.legit_links.items():
            if v['tokens'] == token:
                return k
        return None

    def apply_threshold(self, link, score):
        if score >= .9:
            return link, score
        else:
            return None, score


def main():
    # samples_data_path = 'samples/'
    # phishing_domains_url = 'https://hole.cert.pl/domains/domains.txt'
    legit_domains_file = 'legit_domains.txt'
    scam_domains_file = 'scam_domains.txt'

    # Linki z sampli-niby USELESS, ale mają jeszcze ścieżkę w url
    # scam_links_from_samples = Extractor.extract_links_from_samples(samples_data_path)

    # scam_links_from_url = Extractor.extract_links_from_file(scam_domains_file)
    legit_links_from_file = Extractor.extract_links_from_file(legit_domains_file)

    sim = Similarity(legit_links_from_file)

    url = 'bank.pl'

    result = sim.get_best_match(url)

    print(result)


if __name__ == '__main__':
    main()
