import requests
import json
import os
from redvid import Downloader
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
from Google import Video_Service
from Google import Comment_Service
import time

def AutomatedRVS():
    start = time.time()
    time.sleep(1)
    " Extracting Links & Data From Reddit"
    page = requests.get("https://www.reddit.com/r/popular/top/.json", headers={'User-agent': 'seventhreetwo'}).json()
    page_data = page["data"]["children"]
    page_dist = page["data"]["dist"]

    "Separating Videos From Data"
    count = 0
    while count < page_dist:
        if ((page_data[count]["data"]["is_video"] == True) and (
                page_data[count]["data"]["media"]["reddit_video"]["duration"] <= 60) and (
                page_data[count]["data"]["media"]["reddit_video"]["is_gif"] == False)):
            title = page_data[count]["data"]["title"]
            print(title)
            while (len(title) > 100):
                title_list = title.split()
                title_list.pop()
                title = " ".join(title_list)
            url = page_data[count]["data"]["url"]
            auth = page_data[count]["data"]["author"]
            tags = title.split()
            other_tags = "shorts,youtube shorts,short,youtube shorts video,shorts youtube,youtube short,#shorts,youtube shorts 2021,shorts video youtube,yt shorts,viral shorts,tiktok,youtube vs tiktok,tiktok memes,tiktoks,tiktok 2021,tiktok compilation,best of tiktok,tiktok mashup,tiktok dances 2021,tiktok meme,funny fails,funny videos,funny video,funny videos 2021,funny moments,funny fail,new funny comedy video"
            split_tags = other_tags.split(",")
            combtags = tags + split_tags
            break
        else:
            count += 1
    print(title)
    print(url)
    print(auth)
    
    "Downloading Video From Reddit"
    path = "C:\\Users\\john\\PycharmProjects\\Automated Test\\.auto_video"
    download = Downloader(max_q=True, path=path, url=url)
    download.download()
    file = os.listdir(path)
    video = file[0]
    video_path = path +"\\" + video

    "Uploading Video to Channel With Youtube API"
    CLIENT_SECRET_FILE = "client_secret.json"
    API_NAME = "youtube"
    API_VERSION = "v3"
    UPLOADSCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    upload_service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, UPLOADSCOPES)
    request_body = {
        "snippet": {
            'categoryId': 23,
            'title': title,
            'description': "✔️ Like, Comment, Subscribe and Share for more!!! | Creds: " + auth + " #shorts #meme",
            'tags': split_tags,
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': True,
    }
    mediaFile = MediaFileUpload(video_path)
    upload = upload_service.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=mediaFile
    ).execute()
    video_id = upload["id"]
    end = time.time()
    print("Video: UPLOADED")
    print(end - start)
    return video_path, video_id

def DeleteVideo(video_path, video_id):
    "Delete The Video File After Uploading"

    part_string = "processingDetails"
    CLIENT_SECRET_FILE = "client_secret.json"
    API_NAME = "youtube"
    API_VERSION = "v3"
    REQUESTSCOPES = ["https://www.googleapis.com/auth/youtube"]
    request_service = Video_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, REQUESTSCOPES)

    processingDetails = request_service.videos().list(
        part=part_string,
        id=video_id,
    ).execute()
    if processingDetails["items"][0]["processingDetails"]["processingStatus"] != "succeeded":
        while processingDetails["items"][0]["processingDetails"]["processingStatus"] != "succeeded":
            processingDetails = request_service.videos().list(
                part=part_string,
                id=video_id,
            ).execute()
    os.unlink(video_path)
    print("Video: DELETED")

def Comment(video_id):
    channel_id = "UCKnUNuyEJeoi3XhDwpaJ8nw"
    CLIENT_SECRET_FILE = "client_secret.json"
    API_NAME = "youtube"
    API_VERSION = "v3"
    REQUESTSCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    request_service = Comment_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, REQUESTSCOPES)
    request_body = {
        "snippet": {
            "channelId": channel_id,
            "topLevelComment": {
                "snippet": {
                    "textOriginal": "Thanks for 100 subs 🥳 mext stop is 500! If you would like to subscribe, that would help a lot 👍 I appreciate the suuport regardless 💯 \n- Recomemedur 😁"
                }
            },
            "videoId": video_id
        }
    }
    comment = request_service.commentThreads().insert(
        part="snippet",
        body=request_body
    ).execute()
    print("Comment: POSTED")

video_path, video_id = AutomatedRVS()
DeleteVideo(video_path, video_id)
Comment(video_id)
"""        if (len(title) > 100):
            title_list = list(title)
            while(len(title_list) > 100):
                title_list.pop()
                title = "".join(title_list)"""
"""        if (len(title) > 100):
            while(len(title) > 100):
                title_list = title.split()
                title_list.pop()
                title = " ".join(title_list)"""