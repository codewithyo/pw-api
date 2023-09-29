""" Fetches logged in users details. """

from json import load

from src.pw.credentials import Credentials


class LoggedUser:
    def __init__(self) -> None:
        cookie_dir = Credentials.get_cookie_dir()
        if cookie_dir is None:
            raise FileNotFoundError("Cookie not found.")
        self.cookie_dir = cookie_dir

        # Load cookie data from cookie directory
        data = self.__load_cookie_data()
        self.profile: dict = data["profile"]["data"]
        self.submission = data["submission"]
        self.progress = data["progress"]

    def __load_cookie_data(self) -> dict[str, dict]:
        res = {}
        for file in [i for i in self.cookie_dir.glob("*.json")]:
            res[file.stem] = load(open(file))
        return res
