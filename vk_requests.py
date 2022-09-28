import dev_requests
import config


def vk_post_request(url, method, body) -> dict:
    correct_url = "{vk_api_url}/{vk_api_method}".format(vk_api_url=url,
                                                        vk_api_method=method)
    response = dev_requests.post_request(url=correct_url, body=body)
    return response


def vk_get_group_members_id_list(group_id) -> list:
    url = config.vk_api_request_url
    method = config.vk_get_group_members_method
    body = {
        "v": config.vk_api_v,
        "access_token": config.auth_vk_token,
        "group_id": group_id
    }
    vk_response = vk_post_request(url=url, method=method, body=body)
    members_id_list = vk_response["response"]["items"]
    return members_id_list
