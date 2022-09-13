import requests, re, json
from bs4 import BeautifulSoup
import argparse, cn2an

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}

class BiliIDBase:
    def __init__(self, id):
        self.id = id

class BiliCVBase(BiliIDBase):
    def __init__(self, id):
        super().__init__(id)
    def getBiliCVURL(self):
        return 'https://www.bilibili.com/read/cv' + str(self.id)
    def getBiliCVInfo(self):
        response = requests.get(url=self.getBiliCVURL(), headers=headers)
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find_all(name='meta', attrs={'property': 'og:title'})[0]['content']
        # 仅对换行做了处理，如需进阶处理需参考bs4文档或自行编写
        text = soup.find_all(name='div', attrs={'id': 'article-content'})[0].get_text(separator='\n')
        return title, text

class BiliCV(BiliCVBase):
    def __init__(self, id):
        super().__init__(id)
        self.url = super().getBiliCVURL()
        self.title, self.text = super().getBiliCVInfo()
        
class BiliRLBase(BiliIDBase):
    def __init__(self, id):
        super().__init__(id)
    def getBiliRLURL(self):
        return 'https://www.bilibili.com/read/readlist/rl' + str(self.id)
    def getCVList(self):
        response = requests.get(url=self.getBiliRLURL(), headers=headers)
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        script_to_find = soup.find_all(name='script')
        if not script_to_find: return None
        for script_tag in script_to_find:
            if 'window' in script_tag.text:
                pattern = r'window.articlelistIds = \[.*\]'
                json_text = re.search(r'window.articlelistIds = \[.*\]', script_tag.text).group(0)
                json_text = re.sub(r'window.articlelistIds = ', '', json_text)
                return json.loads(json_text)

class BiliRL(BiliRLBase):
    def __init__(self, id):
        super().__init__(id)
        self.url = super().getBiliRLURL()
        self.cv_id_list = super().getCVList()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('rl_id', help='id of Bilibili Readlist')
    parser.add_argument('--cn2an', help='convert Chinese numbers to Arabic numbers', action='store_true', default=False)
    args = parser.parse_args()
    rl_id = args.rl_id
    #rl_id = 528930 # 测试合集：唐诱？创同人小说 共轭
    rl_obj = BiliRL(rl_id)
    cv_list = [BiliCV(cv_id) for cv_id in rl_obj.cv_id_list]

    for cv in cv_list:
        if args.cn2an:
            # 标题中文数字转换阿拉伯数字，非必须
            cv.title = cn2an.transform(cv.title)
        print(cv.title)
        with open(cv.title + '.txt', 'w', encoding='utf-8') as f:
            f.write(cv.text)