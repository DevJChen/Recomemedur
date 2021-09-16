from TikTokApi import TikTokApi
import os
import json

def AutomatedTVS():
    api = TikTokApi.get_instance(custom_verifyFp="verify_knw4mfwf_wlnkCb1z_IbyS_4vuB_8qnB_dV0pV3LgX1a7")
    amount = 2000
    count = 0
    trendingPage = api.by_trending(count=amount)
    path = "C:\\Users\\john\\PycharmProjects\\Automated Test\\tiktok\\"
    while (count < amount):
        if (trendingPage[count]["video"]["duration"] <= 60 and
                trendingPage[count]["music"]["original"] == True and
                trendingPage[count]["stats"]["playCount"] >= 10000000):
            title = trendingPage[count]["desc"]
            if (len(title) > 100):
                while (len(title) > 100):
                    title_list = title.split()
                    title_list.pop()
                    title = " ".join(title_list)
            if ('\"', "/", ":", "*", "?", '"', "<", ">", "|" in title):
                title = title.replace('\"', '')
                title = title.replace("/", "")
                title = title.replace(":", "")
                title = title.replace("*", "")
                title = title.replace("?", "")
                title = title.replace('"', '')
                title = title.replace("<", "")
                title = title.replace(">", "")
                title = title.replace("|", "")
            tiktok = path + title
            if (os.path.exists(tiktok)):
                print("uploaded tiktok before")
                count+=1
            else:
                url = trendingPage[count]["video"]["downloadAddr"]
                user = trendingPage[count]["author"]["uniqueId"]
                with open(file=tiktok, mode="w") as fp:
                    pass
                print(title)
                print(user)
                print(url)
                break
        else:
            count+=1
AutomatedTVS()




#print(json.dumps(trending, indent=3))
#["id"]
#["author"]["uniqueId"]
#["video"]["duration"]
#["video"]["downloadAddr"]
#['music']["original"]
#["stats"]["playCount"]
#["desc"]
#["authorStats"]["followerCount"]