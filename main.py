from fastapi import FastAPI, Request
from image_comperator import image_comperator
from protocol_checking import protocol_checking

app = FastAPI()


@app.get("/site/")
async def index(url: str):
    try:
        ret = (url, pipelines(url))
    except Exception:
        ret = (url, 'error occured')
    return ret


def pipelines(url):
    result = 0
    weights = {"image_comperator_weight": 0.5, "protocol_weight": 0.5}
    assert sum(weights.values()) == 1
    result += weights["image_comperator_weight"] * image_comperator()
    result += weights["protocol_weight"] * protocol_checking(url)

    return result
