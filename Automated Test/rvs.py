import requests
import json
import os
from redvid import Downloader
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

def AutomatedRVS():
    """ Extracting Links & Data From Reddit"""
    page = requests.get("https://www.reddit.com/r/popular/top/.json", headers={'User-agent': 'seventhreetwo'}).json()
    page_data = page["data"]["children"]
    page_dist = page["data"]["dist"]

    """Separating Videos From Data"""
    count = 0
    while count < page_dist:
        if((page_data[count]["data"]["is_video"] == True) and (page_data[count]["data"]["media"]["reddit_video"]["duration"] <= 60) and (page_data[count]["data"]["media"]["reddit_video"]["is_gif"] == False)):
            title = page_data[count]["data"]["title"]
            print(title)
            if (len(title) > 221):
                title_list = list(title)
                while(len(title_list) > 221):
                    title_list.pop()
                title = "".join(title_list)
            if('\"' in title):
                title = title.replace('\"', '')
            if("/" in title):
                title = title.replace("/", "")
            if(":" in title):
                title = title.replace(":", "")
            if("*" in title):
                title = title.replace("*", "")
            if("?" in title):
                title = title.replace("*", "")
            if('"' in title):
                title = title.replace('"', '')
            if("<" in title):
                title = title.replace("<", "")
            if(">" in title):
                title = title.replace(">", "")
            if("|" in title):
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
    path = "C:\\Users\\john\\Desktop\\.auto_video"
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

    """Delete The Video File After Uploading"""
    video_id = upload["id"]
    part_string = "processingDetails"
    API_NAME2 = "youtube"
    REQUESTSCOPES = ["https://www.googleapis.com/auth/youtube"]
    request_service = Create_Service(CLIENT_SECRET_FILE, API_NAME2, API_VERSION, REQUESTSCOPES)

    upload_response = request_service.videos().list(
        part=part_string,
        id=video_id
    ).execute()
    print(upload_response)

AutomatedRVS()
