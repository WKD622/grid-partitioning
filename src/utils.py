from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def print_infos(function):
    def wrapper(*args, **kwargs):
        # print(function.__name__ + " started")
        out = function(*args, **kwargs)
        print(function.__name__ + " finished")
        return out

    return wrapper
