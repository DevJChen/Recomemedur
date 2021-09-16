import redvid
import os
import ffmpeg
import requests
import json
from redvid import Downloader

page = requests.get("https://www.reddit.com/r/funny/comments/m9btq6/wheres_your_mask_prank/.json", headers={'User-agent': 'seventhreetwo'}).json()
links = json.dumps(page, indent=2)
page_data = page[0]
data = page_data["data"]["children"]
title = data[0]["data"]["title"]
print(title)
if (("\'" in title) or ("\'" in title)):
    #title = title.replace("\'", "")
    title = title.replace('\"', "")
    title = title.replace("?", "")
    print(title)
    path = "C:\\Users\\john\\Desktop\\.auto_video"
reddit = Downloader(max_q=True,path= "C:/Users/john/Desktop/.auto_video")
reddit.url = 'https://v.redd.it/kwg1214qfko61'
reddit.download()
path = reddit.file_name
other_path = "C:\\Users\\john\\Desktop\\.auto_video"
video_name = "\\" + title + ".mp4"
final_path = other_path+video_name
print(final_path)
#video = os.rename(reddit.file_name, final_path)

