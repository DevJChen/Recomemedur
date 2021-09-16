import requests
import json
import os
from redvid import Downloader
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
from Google import Video_Service
from Google import Comment_Service
from moviepy.editor import VideoFileClip, concatenate_videoclips
import time

def AutomatedRVS():
    start = time.time()
    time.sleep(1)
    " Extracting Links & Data From Reddit"
    page = requests.get("https://www.reddit.com/r/Unexpected/top/.json", headers={'User-agent': '0938423897'}).json()
    page_data = page["data"]["children"]
    page_dist = page["data"]["dist"]

    "Separating Videos From Data"
    count = 0
    counter = 0
    authList = []
    urlList = []
    titleList = []
    while count < page_dist:
        if ((page_data[count]["data"]["is_video"] == True) and (
                page_data[count]["data"]["media"]["reddit_video"]["duration"] <= 20) and (
                page_data[count]["data"]["media"]["reddit_video"]["is_gif"] == False)):
            title = page_data[count]["data"]["title"]
            if counter == 3:
                break
            while (len(title) > 100):
                title_list = title.split()
                title_list.pop()
                title = " ".join(title_list)
            print(title)
            url = page_data[count]["data"]["url"]
            auth = page_data[count]["data"]["author"]
            print(url)
            print(auth)
            titleList.extend(title.split(" "))
            authList.append(auth)
            urlList.append(url)
            counter += 1
            count += 1
        else:
            count += 1
    other_tags = "compilation,shorts,shorts compilation,video compilation,mrbeast compilation,youtube shorts compilation"
    split_tags = other_tags.split(",")
    split_tags.extend(titleList)
    creds = ", ".join(authList)

    "Downloading Video From Reddit"
    print(counter)
    path = "/home/ubuntu/.auto_video"
    finalvideopath = "/home/ubuntu/.finishedvideo/comp.mp4"
    for link in urlList:
        download = Downloader(max_q=True, path=path, url=link)
        download.download()

    "Creating Compilation Video"
    pathList = []
    for file in os.listdir(path):
        video_path = path +"/" + file
        vc = VideoFileClip(video_path)
        pathList.append(vc)
    print(pathList)
    final_video = concatenate_videoclips(pathList)
    final_video.write_videofile(finalvideopath)
    print("VIDEO: COMPILATED")

    "Delete Video Afterwards"
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        os.unlink(file_path)

    "Uploading Video to Channel With Youtube API"
    CLIENT_SECRET_FILE = "client_secret.json"
    API_NAME = "youtube"
    API_VERSION = "v3"
    UPLOADSCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    upload_service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, UPLOADSCOPES)
    request_body = {
        "snippet": {
            'categoryId': 23,
            'title': "Short Shorts Compilation",
            'description': "✔️ Like, Comment, Subscribe and Share for more!!! | Creds: " + creds + " #shorts #meme",
            'tags': split_tags,
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': True,
    }
    mediaFile = MediaFileUpload(finalvideopath)
    upload = upload_service.videos().insert(
        part="snippet,status",
        notifySubscribers=True,
        body=request_body,
        media_body=mediaFile
    ).execute()
    video_id = upload["id"]
    end = time.time()
    print("Video: UPLOADED")
    print(end - start)
    return finalvideopath, video_id

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
                    "textOriginal": "If you would like to subscribe or drop a like, that would help a lot 👍 I appreciate the support regardless 💯 \n- Recomemedur 😁"
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

finalvideopath, video_id = AutomatedRVS()
DeleteVideo(finalvideopath, video_id)
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