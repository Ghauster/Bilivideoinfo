import re
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

def write_error_log(message):
    with open("video_errorlist.txt", "a") as file:
        file.write(message + "\n")

def is_url(video_id_or_url):
    return video_id_or_url.startswith("http") or video_id_or_url.startswith("https")

def get_video_url(video_id_or_url):
    if is_url(video_id_or_url):
        return video_id_or_url
    else:
        return f"https://www.bilibili.com/video/{video_id_or_url}"

input_file = "idlist.txt"
output_file = "output.xlsx"

new_wb = Workbook()
new_ws = new_wb.active
new_ws.append(
    ["标题", "链接", "up主", "up主id", "精确播放数", "历史累计弹幕数", "点赞数", "投硬币枚数", "收藏人数", "转发人数",
     "发布时间", "视频时长(秒)", "视频简介", "作者简介", "标签", "视频aid"])

with open(input_file, "r") as file:
    id_list = file.readlines()

i = 0
for video_id_or_url in id_list:
    i += 1
    url = get_video_url(video_id_or_url.strip())
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # 视频 aid、视频时长和作者 id
        initial_state_script = soup.find("script", text=re.compile("window.__INITIAL_STATE__"))
        initial_state_text = initial_state_script.string

        author_id_pattern = re.compile(r'"mid":(\d+)')
        video_aid_pattern = re.compile(r'"aid":(\d+)')
        video_duration_pattern = re.compile(r'"duration":(\d+)')

        author_id = author_id_pattern.search(initial_state_text).group(1)
        video_aid = video_aid_pattern.search(initial_state_text).group(1)
        video_duration_raw = int(video_duration_pattern.search(initial_state_text).group(1))
        video_duration = video_duration_raw - 2

        # 提取标题
        title_raw = soup.find("title").text
        title = re.sub(r"_哔哩哔哩_bilibili", "", title_raw).strip()

        # 提取标签
        keywords_content = soup.find("meta", itemprop="keywords")["content"]
        content_without_title = keywords_content.replace(title + ',', '')
        keywords_list = content_without_title.split(',')
        tags = ",".join(keywords_list[:-4])

        meta_description = soup.find("meta", itemprop="description")["content"]
        numbers = re.findall(
            r'[\s\S]*?视频播放量 (\d+)、弹幕量 (\d+)、点赞数 (\d+)、投硬币枚数 (\d+)、收藏人数 (\d+)、转发人数 (\d+)',
            meta_description)

        # 提取作者
        author_search = re.search(r"视频作者\s*([^,]+)", meta_description)
        if author_search:
            author = author_search.group(1).strip()
        else:
            author = "未找到作者"

        # 提取作者简介
        author_desc_pattern = re.compile(r'作者简介 (.+?),')
        author_desc_match = author_desc_pattern.search(meta_description)
        if author_desc_match:
            author_desc = author_desc_match.group(1)
        else:
            author_desc = "未找到作者简介"

        # 提取视频简介
        meta_parts = re.split(r',\s*', meta_description)
        if meta_parts:
            video_desc = meta_parts[0].strip()
        else:
            video_desc = "未找到视频简介"

        if numbers:
            views, danmaku, likes, coins, favorites, shares = [int(n) for n in numbers[0]]
            publish_date = soup.find("meta", itemprop="uploadDate")["content"]
            new_ws.append([title, url, author, author_id, views, danmaku, likes, coins, favorites, shares, publish_date, video_duration, video_desc, author_desc, tags, video_aid])
            print(f"第{i}行视频{url}已完成爬取")
        else:
            print(f"第{i}行视频 {url}未找到相关数据，可能为分集视频")

    except Exception as e:
        write_error_log(f"第{i}行视频发生错误：{e}")
        print(f"第{i}行发生错误，已记录到错误日志:出错数据为{video_id_or_url}")

new_wb.save(output_file)
