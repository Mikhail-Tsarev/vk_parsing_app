import time


def get_unix_time(date):
    try:
        return int(
            time.mktime(time.strptime(f"{date} 00:00:00", "%Y-%m-%d %H:%M:%S"))
        )
    except ValueError:
        return 0


def get_domain(link: str):
    return link.strip("/").split("/")[-1]
