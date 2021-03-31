from Google import Create_Service
from Google import Video_Service
from pprint import pprint
import requests

CLIENT_SECRET_FILE = "client_secret.json"
API_NAME = "youtube"
API_VERSION = "v3"
REQUESTSCOPES = ["https://www.googleapis.com/auth/youtube"]

request_service = Video_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, REQUESTSCOPES)

part_string = "processingDetails"
video_id = "V0dTUgFC76A"

data = request_service.videos().list(
    part = part_string,
    id = video_id
).execute()

pprint(data["items"][0]["processingDetails"]["processingStatus"])