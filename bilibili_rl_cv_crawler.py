import requests
from lxml import etree
import argparse
import cn2an
from pathlib import Path

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
}


class BiliCV:
    id: int
    url: str
    title: str
    text: str

    def __init__(self, id: int):
        self.id = id
        self.text = ""
        self._build_url()
        self._build_info()

    def _build_url(self):
        self.url = f"https://www.bilibili.com/read/cv{self.id}"

    def _build_info(self):
        response = requests.get(url=self.url, headers=headers)
        if response.status_code != 200:
            raise Exception("Not right return data")

        parser = etree.HTML(response.content.decode("utf-8"))
        self.title = parser.xpath('.//meta[@property="og:title"]')[0].attrib["content"]

        # 仅对换行做了处理，如需进阶处理需自行编写
        paragraphs = parser.xpath(
            './/div[@id="article-content"]/div[@id="read-article-holder"]/p'
        )
        for paragraph in paragraphs:
            text = paragraph.text
            self.text += text if text is not None else "\n"

        if self.text.startswith("'"):
            self.text = self.text[1:]
        if self.text.endswith("'"):
            self.text = self.text[:-1]


class BiliRL:
    id: int
    url: str
    api_url: str
    cvid_list: list[int]

    def __init__(self, id: int):
        self.id = id
        self.cvid_list = []

        self._build_url()
        self._build_api_url()
        self._build_cvid_list()

    def _build_url(self):
        self.url = f"https://www.bilibili.com/read/readlist/rl{self.id}"

    def _build_api_url(self):
        self.api_url = (
            f"https://api.bilibili.com/x/article/list/web/articles?id={self.id}"
        )

    def _build_cvid_list(self):
        response = requests.get(url=self.api_url, headers=headers)
        if response.status_code != 200:
            return

        jsondata = response.json()
        cv_list = jsondata["data"]["articles"]
        self.cvid_list = [cv["id"] for cv in cv_list]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("rl_id", help="id of Bilibili Readlist")
    parser.add_argument(
        "--cn2an",
        help="convert Chinese numbers to Arabic numbers",
        action="store_true",
        default=False,
    )
    parser.add_argument("--output-dir", help="set output folder", default="./output")
    args = parser.parse_args()
    rl_id = args.rl_id
    output_dir = args.output_dir
    # rl_id = 528930  # 测试合集：唐诱？创同人小说 共轭
    rl_obj = BiliRL(rl_id)
    cv_list = [BiliCV(cv_id) for cv_id in rl_obj.cvid_list]

    for cv in cv_list:
        if args.cn2an:
            # 标题中文数字转换阿拉伯数字，非必须
            cv.title = cn2an.transform(cv.title)
        print(cv.title)
        cv_path = Path(f"{output_dir}/{cv.title}.txt")
        with cv_path.open("w", encoding="utf-8") as f:
            f.write(cv.text)
