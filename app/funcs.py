import json
import os
import time

import vk_api

from vk_token import token


def get_unix_time(date):
    return int(
        time.mktime(time.strptime(f"{date} 00:00:00", "%Y-%m-%d %H:%M:%S"))
    )


def dump_to_json(data: list, filename: str) -> None:
    """
    Saves info from list of dicts to json file
    :param data: List of dicts to dump info
    :param filename: Name of resulting json file
    """

    full_file_name = os.getcwd() + "\\" + "data" + "\\" + filename + ".json"
    with open(full_file_name, "w") as f_out:
        json.dump(data, f_out)


def get_all_posts(domain: str, token: str, date) -> list:
    all_posts = []
    offset = 0
    flag = True
    while flag:
        session = vk_api.VkApi(token=token)
        vk = session.get_api()
        response = vk.wall.get(domain=domain, count=100, offset=offset)
        dump_to_json(response["items"][6], "post3")
        for item in response["items"]:
            if item["date"] < date and item is not response["items"][0]:
                flag = False
                break
            all_posts.append(item)

        offset += 100
        time.sleep(0.2)

    return all_posts


def get_domain(link: str):
    return link.strip("/").split("/")[-1]


if __name__ == "__main__":
    link1 = "https://vk.com/marinkaapelsinka"
    link2 = "https://vk.com/id254649273"
    l = get_all_posts(get_domain(link1), token, 1633035600)
    cnt = 0

    for el in l:
        print(cnt, "----", el["text"])
        if "attachments" in el.keys():
            for attach in el["attachments"]:
                print(
                    f'vk.com/{attach["type"]}{attach[attach["type"]]["owner_id"]}_{attach[attach["type"]]["id"]}'
                )
        cnt += 1
