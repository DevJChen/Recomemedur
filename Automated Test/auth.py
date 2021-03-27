from Google import Create_Service

CLIENT_SECRET_FILE = "client_secret.json"
API_NAME = "youtube"
API_NAME2 = "youtubeData"
API_VERSION = "v3"
UPLOADSCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET_FILE2 = "client_secret.json"
REQUESTSCOPES = ["https://www.googleapis.com/auth/youtube"]

request_service = Create_Service(CLIENT_SECRET_FILE, API_NAME2, API_VERSION, REQUESTSCOPES)