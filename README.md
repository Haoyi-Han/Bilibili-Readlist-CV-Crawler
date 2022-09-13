# 哔哩哔哩（Bilibili）专栏文集爬取工具

## 简介
本工具用于爬取B站专栏文集，遍历文集中各文章 cv 号并将相应文本内容（无图片）保存到以文章标题为文件名的文本文档中。

## 用法
用以下命令克隆本项目：
```shell
git clone https://github.com/Haoyi-Han/Bilibili-Readlist-CV-Crawler.git
cd Bilibili-Readlist-CV-Crawler
```

安装必要运行库：
```shell
pip install -r requirements.txt
```

运行命令：
```shell
python -m bilibili-rl-cv-crawler <专栏文集id>
```

若需要将爬取文章的标题序号化（即从中文数字转换为阿拉伯数字，便于排序管理），请添加 `--cn2an` 参数：
```shell
python -m bilibili-rlcv-crawler <专栏文集id> --cn2an
```

爬取的文章将以文章标题为文件名，以 `.txt` 格式保存在脚本所在目录下。
