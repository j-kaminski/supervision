from random import randint
from fastapi import FastAPI, Request
from image_comperator import image_comperator

app = FastAPI()


@app.get("/site/")
async def index(url: str):
    return (url, image_comperator(legit_adress='assets/alior-legit.png'))
