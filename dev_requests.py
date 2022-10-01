import requests


def post_request(url: str, body: dict = "") -> dict:
    response = requests.post(url=url, params=body)
    return response.json()


def get_request(url: str, body: dict = "") -> dict:
    response = requests.get(url=url, headers=body)
    return response.json()
