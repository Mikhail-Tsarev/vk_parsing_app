import json
import os
import time

import vk_api

from vk_token import token


def dump_to_json(data: list, filename: str) -> None:
    """
    Saves info from list of dicts to json file
    :param data: List of dicts to dump info
    :param filename: Name of resulting json file
    """

    full_file_name = os.getcwd() + "\\" + "data" + "\\" + filename + ".json"
    with open(full_file_name, "w") as f_out:
        json.dump(data, f_out)


def post_count(domain: str, token: str) -> int:
    session = vk_api.VkApi(token=token)
    vk = session.get_api()
    response = vk.wall.get(domain=domain, count=50, offset=0)
    dump_to_json(response["items"][3], "post1")

    return response["count"]


def get_all_posts(domain: str, token: str, cnt) -> list:
    all_posts = []
    offset = 0
    times = cnt // 100 + 1
    for i in range(times):
        session = vk_api.VkApi(token=token)
        vk = session.get_api()
        response = vk.wall.get(domain=domain, count=100, offset=offset)
        all_posts.extend(response["items"])
        print(len(all_posts))
        offset += 100
        time.sleep(0.2)

    return all_posts


def get_link():
    return "marinkaapelsinka"


if __name__ == "__main__":
    # link = "marteleur"
    link = get_link()
    cnt = post_count(link, token)
    # l = get_all_posts(link, token, cnt)
    # print(cnt)
    # print(len(l))
