import os
import time
import json
from TikTokApi import TikTokApi

start = time.time()
time.sleep(1)
api = TikTokApi.get_instance(custom_verifyFp="verify_ko4syt8j_IQnuDlVm_vKwF_4TyJ_93ZD_FX0roM6MnLa0")
amount = 2000
count = 0
counter = 0
view = 0
trendingPage = api.by_trending(count=amount)
#print(json.dumps(trendingPage, indent=3))
while count < amount:
    view += trendingPage[count]["stats"]["playCount"]
    if trendingPage[count]["stats"]["playCount"] >= 10000000:
        print(counter)
        print(trendingPage[count]["authorStats"]["followerCount"])
        print(trendingPage[count]["video"]["downloadAddr"])
        counter+=1
        count+=1
    else:
        count+=1
avgview = view/amount
print(counter)
print(avgview)
end = time.time()
print(end-start)


"""api = TikTokApi.get_instance(custom_verifyFp="verify_knw4mfwf_wlnkCb1z_IbyS_4vuB_8qnB_dV0pV3LgX1a7")
amount = 1
trendingPage = api.by_trending(count=amount)
print(json.dumps(trendingPage, indent=3))"""

"""path = "C:\\Users\\john\\PycharmProjects\\Automated Test\\tiktok\\"
ass = "ass"
os.path.exists(path)
with open(file=path+ass, mode="w") as fp:
    pass"""
