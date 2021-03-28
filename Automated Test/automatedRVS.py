from rvs import AutomatedRVS
from rvs import deleteVideo
import time
import schedule

schedule.every().day.at("13:59").do(AutomatedRVS)
schedule.every().day.at("13:55").do(deleteVideo)

while True:
    schedule.run_pending()
    time.sleep(1)
