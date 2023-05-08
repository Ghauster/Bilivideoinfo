# B站视频信息爬虫

Bilibili 视频数据爬虫，能**批量**爬取指定视频的信息。
#### 好用的话记得给个star

## 亮点

- 爬取的数据**全面**：包括：**标题**、**链接**、**up主**、**up主id**、**精确播放数**、**历史累计弹幕数**、**点赞数**、**投硬币枚数**、**收藏人数**、**转发人数**、**发布时间**、**视频时长(秒)**、**视频简介**、**作者简介**、**标签**（分区、参与的创作活动等等内容也都会成为视频的标签）和**视频aid**
![image](https://github.com/Ghauster/Bilivideoinfo/blob/main/output-sample.png)

- 爬取的是**精确**数据：例如，播放数是精确的数值（如 123456，而非 12.3 万）

## 使用方法

1. 将需要爬取的**视频链接**（http或https开头）或**视频 ID**（bid） 列表存储在名为 `idlist.txt` 的文件中，每行一个
2. 运行 `python scraper.py`
3. 爬取的数据将保存到名为 `output.xlsx` 的 Excel 文件中
4. 如果有出错，出错的记录会保存到video_errorlist.txt中

## 注意事项

- **不用登录**，但请确保网络畅通
- 请确保在运行代码之前已安装所需的 Python 库（如 requests、beautifulsoup4 和 openpyxl）
