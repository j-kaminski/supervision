from fastapi import FastAPI, Request
from image_comperator import image_comperator
from protocol_checking import protocol_checking
from website_ss import website_ss

app = FastAPI()


@app.get("/site/")
async def index(url: str):
    try:
        ret = (url, pipelines(url))
    except Exception:
        ret = (url, 'error occured')
    return ret

legit_ss = None
scam_ss = None

def pipelines(url):
    result = 0
    weights = {"image_comperator_weight": 0.5, "protocol_weight": 0.5}
    assert sum(weights.values()) == 1
    if "modul_radka":
        legit_ss = website_ss(url)
        result += weights["image_comperator_weight"] * image_comperator(legit_img=legit_ss, scam_img=legit_ss)
    result += weights["protocol_weight"] * protocol_checking(url)

    return result
