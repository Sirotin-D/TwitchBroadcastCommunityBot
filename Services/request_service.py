import requests
from requests import RequestException


class RequestService:
    @staticmethod
    def post_request(url: str, body: dict = "") -> dict:
        response = requests.post(url=url, params=body)
        if response.status_code != 200:
            raise RequestException(f"Error request. Status code: {response.status_code}")
        else:
            return response.json()

    @staticmethod
    def get_request(url: str, body: dict = "") -> dict:
        response = requests.get(url=url, headers=body)
        if response.status_code != 200:
            raise RequestException(f"Error request. Status code: {response.status_code}")
        else:
            return response.json()
