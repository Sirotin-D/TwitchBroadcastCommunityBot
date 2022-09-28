import requests


def vk_get_request():
    url = "https://api.vk.com/method/groups.getMembers?v={}&&access_token={}&group_id={}".format(config.vk_api_v,
                                                                                                 config.auth_VK_token,
                                                                                                 config.vk_test_group_id)
    response = requests.get(url=url)
    return response.json()["response"]

def get_vk_user_id():
    vk_response = vk_get_request()
    members_id_list = vk_response["items"]
    return members_id_list

