from rvs import AutomatedRVS
from rvs import deleteVideo
import time
import schedule

schedule.every().day.at("08:00").do(AutomatedRVS)
schedule.every().day.at("08:02").do(deleteVideo)

while True:
    schedule.run_pending()
    time.sleep(1)
