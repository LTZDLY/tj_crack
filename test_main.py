from datetime import datetime
from functools import wraps
import json
import time
from crack import check, crack, encrypt
import requests


def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction(*args, **kwargs):
        print(f"[{datetime.now()}] ", end="")
        t1 = time.time_ns()
        data = a_func(*args, **kwargs)
        print(f"{a_func.__name__}: cost: {(time.time_ns() - t1) / 10**6}ms")
        return data

    return wrapTheFunction


def getData(s: requests.Session):
    resp = s.post(
        url="https://ids.tongji.edu.cn:8443/nidp/app/login?sid=0&sid=0/getCaptcha=1"
    )
    return resp.json()["repData"]


@a_new_decorator
def crack_main(s: requests.Session):
    data = getData(s)
    point = crack(data)
    res = check(data, point)
    print(res)
    if res["repCode"] == "0000":
        return encrypt(
            data["token"] + "---" + json.dumps(point).replace(" ", ""),
            data["secretKey"],
        )


if __name__ == "__main__":
    for _ in range(20):
        s = requests
        try:
            print(crack_main(s))
        except:
            ...
