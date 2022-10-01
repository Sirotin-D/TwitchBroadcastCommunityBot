from dev_requests import RequestService
import config


def vk_post_request(url: str, method: str, body: dict) -> dict:
    correct_url: str = "{vk_api_url}/{vk_api_method}".format(vk_api_url=url,
                                                             vk_api_method=method)
    response: dict = RequestService.post_request(url=correct_url, body=body)
    return response


def vk_get_group_members_id_list(group_id: str) -> list:
    url: str = config.vk_api_request_url
    method: str = config.vk_get_group_members_method
    body: dict = {
        "v": config.vk_api_version,
        "access_token": config.vk_test_access_token,
        "group_id": group_id
    }
    vk_response: dict = vk_post_request(url=url, method=method, body=body)
    members_id_list: list = vk_response["response"]["items"]
    return members_id_list
