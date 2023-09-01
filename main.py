import json
import traceback

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from crack import check, crack, encrypt

app = FastAPI(
    # root_path="/seproject"
    openapi_url=None,
    # docs_url=None,
    redoc_url=None,
)


class CrackData(BaseModel):
    originalImageBase64: str
    result: bool
    secretKey: str
    token: str
    wordList: list


class CheckData(BaseModel):
    secretKey: str
    token: str
    point: list


@app.post("/tj_crack")
async def fun(data: CrackData):
    try:
        d = data.dict()
        point = crack(d)
        return {
            "point": point,
            "enc": encrypt(json.dumps(point).replace(" ", ""), d["secretKey"]),
        }
    except:
        traceback.print_exc()
        return None


@app.post("/tj_check")
async def fun(data: CheckData):
    try:
        d = data.dict()
        return encrypt(
            d["token"] + "---" + json.dumps(d["point"]).replace(" ", ""),
            d["secretKey"],
        )
    except:
        traceback.print_exc()
        return None


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000)
