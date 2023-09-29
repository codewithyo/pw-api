"""
Use for fetching/downloading the data using PW APIs.

Also store the files in respective paths in JSON format.
"""

from json import dump, load, loads
from pathlib import Path
from time import sleep
from typing import Any, Literal, TypeAlias

from bs4 import BeautifulSoup
from requests import get

from src import LiveCourse
from src.core.logger import get_logger

UrlType: TypeAlias = Literal["quiz", "assignment"]
logger = get_logger(__name__)


class PWApi:
    def __init__(self, auth_key: str, course_id: str) -> None:
        self.auth_key = auth_key
        self.cid = course_id

    def get(self, url: str) -> dict[str, Any]:
        """Get JSON response from the provided PW API `URL` using `auth_key`"""
        headers = {
            "Origin": "https://learn.pwskills.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://learn.pwskills.com/",
            "Authorization": self.auth_key,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
        }
        r = get(url, headers=headers, timeout=3)

        r.raise_for_status()
        return r.json()

    def _id_from_url(self, url: str) -> str:
        return url.rsplit("/", 1)[-1]

    def generate_fp(self, type: UrlType) -> Path:
        fp = Path("data") / type
        return fp / f"{type}_{self.cid}.json"

    def export_data(
        self,
        cname: str,
        type_: UrlType,
        wait: float = 2,
    ) -> None:
        """
        Stores quizzes and assignments in JSON format.
        Also, excludes the URL which are already downloaded and stored in the directory.
        """
        url_list: list[str] = self.__get_ids_to_download(cname, type_)
        fp = self.generate_fp(type_)
        stored_ids = self.load_downloaded_ids(fp) if fp.exists() else []
        res: list = load(open(fp)) if fp.exists() else []

        logger.info(
            f"No. of {type_!r} left to fetch: %s", (len(url_list) - len(stored_ids))
        )
        try:
            count = 0
            dump_counter = 0
            for url in url_list:
                if self._id_from_url(url) in stored_ids:
                    continue

                if type_ == "quiz":
                    sleep(wait)
                    logger.info(f"{type_.title()}[{count}/{len(url_list)}]: {url}")
                    res.append(self.get_quiz_data(url))
                elif type_ == "assignment":
                    sleep(wait)
                    logger.info(f"{type_.title()}[{count}/{len(url_list)}]: {url}")
                    res.append(self.get_assignment_data(url))
                else:
                    raise TypeError("Argument type_ must either quiz or assignment.")

                if dump_counter > 20:
                    logger.info('Dumping at "%s"', fp)
                    res = sorted(res, key=lambda x: x["createdAt"])
                    dump(res, open(fp, "w"), indent=2)

                    logger.info('Loading from "%s"', fp)
                    res: list = load(open(fp)) if fp.exists() else []

                count += 1
                dump_counter += 1

        except Exception as e:
            logger.error(e)
            raise

        finally:
            logger.info('Dumping at "%s"', fp)
            res = sorted(res, key=lambda x: x["createdAt"])
            dump(res, open(fp, "w"), indent=2)

    def __get_live_course_dict(self, cname: str):
        url = f"https://learn.pwskills.com/course/{cname.replace(' ', '-')}/{self.cid}"
        r = get(url)
        logger.info("GET[%s]: %s", r.status_code, r.url)

        soup = BeautifulSoup(r.text, "html.parser")
        script = soup.find("script", {"id": "__NEXT_DATA__"})

        if script:
            data = script.text
        else:
            raise TypeError(
                "Required script tag is not available for the available course url."
            )
        return loads(data)["props"]["pageProps"]

    def __get_ids_to_download(self, cname: str, type_: UrlType) -> list[str]:
        cdata = self.__get_live_course_dict(cname)
        lc = LiveCourse(**cdata)
        df = lc.merged_df(self.cid)
        return df.query("type==@type_")["url"].tolist()

    def load_downloaded_ids(self, fp: Path) -> list[str]:
        """Returns ID of all downloaded Quizzes and Assignments."""
        ids = []
        data = load(open(fp))
        for d in data:
            ids.append(d["_id"])
        return ids

    def get_assignment_data(self, url: str) -> dict[str, Any]:
        data = self.get(url)["data"]

        solution_link = None
        user_sub = data.get("userSubmission", None)
        if user_sub is not None:
            solution_link = user_sub["assignmentSubmission"]["data"]["url"]

        res = {
            "_id": data["lesson"]["_id"],
            "title": data["lesson"]["title"],
            "data": data["lesson"]["data"],
            "solution": solution_link,
            "createdAt": data["lesson"]["createdAt"],
        }
        return res

    def get_quiz_data(self, url: str) -> dict[str, Any]:
        data = self.get(url)["data"]
        res = {
            "_id": data["lesson"]["_id"],
            "title": data["lesson"]["title"],
            "quizQuestions": data["lesson"]["quizQuestions"],
            "createdAt": data["lesson"]["createdAt"],
        }
        return res

    def update_solution_links(self, force_update: bool = False) -> None:
        """Update existing assignments' solution link."""
        fp = self.generate_fp("assignment")

        logger.info('Load data from "%s"', fp)
        data: list[dict] = load(open(fp))

        try:
            count = 0
            for d in data:
                if d["solution"] is not None:
                    if not force_update:
                        continue

                url = f'https://api.pwskills.com/v1/learn/lesson/course/{self.cid}/{d["_id"]}'
                new_link = self.get_assignment_data(url)["solution"]
                if new_link is not None:
                    count = count + 1
                    d["solution"] = new_link

                    print(new_link)
                    logger.info("Storing solution url for Assignment: %s", new_link)
                else:
                    logger.warning("No solution for Assignment: %s", url)
                sleep(0.5)

                if count > 20:
                    logger.info('Dump data at "%s"', fp)
                    dump(data, open(fp, "w"), indent=2)

                    logger.info('Load data from "%s"', fp)
                    data: list[dict] = load(open(fp))
                    count = 0
        finally:
            logger.info('Dump data at "%s"', fp)
            dump(data, open(fp, "w"), indent=2)
