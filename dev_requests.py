import requests


def post_request(url, data) -> dict:
    response = requests.post(url=url, json=data)
    return response.json()


def get_request(url, data) -> dict:
    response = requests.get(url=url, headers=data)
    return response.json()
