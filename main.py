from fastapi import FastAPI, Request
from image_comperator import image_comperator
from protocol_checking import protocol_checking
from website_ss import website_ss
from parser import Similarity, Extractor

app = FastAPI()


@app.get("/site/")
async def index(url: str):
    try:
        ret = (url, pipelines(url))
    except Exception as e:
        ret = (url, f'error occured: {e}')
    return ret


legit_ss = None
scam_ss = None
legit_domains_file = 'legit_domains.txt'
scam_domains_file = 'scam_domains.txt'

# Linki z sampli-niby USELESS, ale mają jeszcze ścieżkę w url
# scam_links_from_samples = Extractor.extract_links_from_samples(samples_data_path)

# scam_links_from_url = Extractor.extract_links_from_file(scam_domains_file)
legit_links_from_file = Extractor.extract_links_from_file(legit_domains_file)
sim = Similarity(legit_links_from_file, threshold=0.8)


def pipelines(url):
    result = 0
    weights = {"image_comperator_weight": 0.5, "protocol_weight": 0.5}
    matched_legit = sim.get_best_match(url)
    print(f"matched_legit {matched_legit[0]}")
    if matched_legit[0]:
        legit_ss = website_ss(matched_legit[0])
        print("legit_ss")
        scam_ss = website_ss(url)
        print("scam_ss")
        result += weights["image_comperator_weight"] * image_comperator(
            legit_img=legit_ss, scam_img=scam_ss)
        print("comperator")
    else:
        checked = []
        scam_ss = website_ss(url)
        print("scam_ss")
        for legit in legit_links_from_file:
            print(f"comparison with {legit}")
            legit_ss = website_ss(legit)
            print("legit_ss")
            checked.append(
                image_comperator(scam_img=scam_ss, legit_img=legit_ss))
        result += weights["image_comperator_weight"] * max(checked)
        print("comparison finished")

    result += weights["protocol_weight"] * protocol_checking(url)
    print("protocol")

    return result
