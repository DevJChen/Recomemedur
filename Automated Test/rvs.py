import requests
import json
import os
from redvid import Downloader
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
from Google import Video_Service
import time

def AutomatedRVS():
    start = time.time()
    time.sleep(1)
    """ Extracting Links & Data From Reddit"""
    page = requests.get("https://www.reddit.com/r/popular/top/.json", headers={'User-agent': 'seventhreetwo'}).json()
    page_data = page["data"]["children"]
    page_dist = page["data"]["dist"]

    """Separating Videos From Data"""
    count = 0
    while count < page_dist:
        if ((page_data[count]["data"]["is_video"] == True) and (
                page_data[count]["data"]["media"]["reddit_video"]["duration"] <= 60) and (
                page_data[count]["data"]["media"]["reddit_video"]["is_gif"] == False)):
            title = page_data[count]["data"]["title"]
            print(title)
            if (len(title) > 100):
                while (len(title) > 100):
                    title_list = title.split()
                    title_list.pop()
                    title = " ".join(title_list)
                if ('\"' in title):
                    title = title.replace('\"', '')
                if ("/" in title):
                    title = title.replace("/", "")
                if (":" in title):
                    title = title.replace(":", "")
                if ("*" in title):
                    title = title.replace("*", "")
                if ("?" in title):
                    title = title.replace("*", "")
                if ('"' in title):
                    title = title.replace('"', '')
                if ("<" in title):
                    title = title.replace("<", "")
                if (">" in title):
                    title = title.replace(">", "")
                if ("|" in title):
                    title = title.replace("|", "")
            url = page_data[count]["data"]["url"]
            auth = page_data[count]["data"]["author"]
            tags = title.split()
            break
        else:
            count += 1
    print(title)
    print(url)
    print(auth)

    """Downloading Video From Reddit"""
    path = "C:\\Users\\john\\PycharmProjects\\Automated Test\\.auto_video"
    video_title = title + ".mp4"
    video_path = "\\" + video_title
    new_path = path + video_path
    download = Downloader(max_q=True, path=path, url=url)
    download.download()
    os.rename(download.file_name, new_path)

    """Uploading Video to Channel With Youtube API"""
    CLIENT_SECRET_FILE = "client_secret.json"
    API_NAME = "youtube"
    API_VERSION = "v3"
    UPLOADSCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    upload_service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, UPLOADSCOPES)
    request_body = {
        "snippet": {
            'categoryId': 24,
            'title': title,
            'description': "Like, Comment, Share, Subscribe for more!!! | Creds: " + auth,
            'tags': tags,
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': True,
    }
    mediaFile = MediaFileUpload(new_path)
    upload = upload_service.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=mediaFile
    ).execute()
    video_id = upload["id"]
    end = time.time()
    print(end - start)
    return new_path, video_id

def DeleteVideo(new_path, video_id):
    """Delete The Video File After Uploading"""

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
    print("starting to delete process")
    while os.path.exists(new_path):
        try:
            os.remove(new_path)
        except:
            print("trying again")
    print("video has been uploaded and deleted")

new_path, video_id = AutomatedRVS()
DeleteVideo(new_path, video_id)

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