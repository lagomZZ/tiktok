import threading
from concurrent.futures import ThreadPoolExecutor
import random

import requests,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

pool = ThreadPoolExecutor(max_workers=5)

def start_task(ads_id,comments,studio_url_queue,is_dynamic,comment_num,comment_interval,each_group_studio_num):
    # 操控浏览器
    retry_times = 0
    open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + ads_id
    close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + ads_id
    try:
        randon_sleep = random.randint(1, 5)
        print(ads_id + "-随机延时：" + str(randon_sleep))
        time.sleep(randon_sleep)

        resp = requests.get(open_url).json()
        print(resp)


        while( resp["code"] == -1):
                if retry_times > 2:
                    print(ads_id + "重试次数过多")
                    break
                retry_times = retry_times + 1
                print(ads_id+"重试"+str(retry_times))
                time.sleep(2)
                open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + ads_id
                resp = requests.get(open_url).json()
                print(resp)

        chrome_driver = resp["data"]["webdriver"]
        print(ads_id+'good')
        print(open_url)
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])

    except Exception as e:
        print(e)

        print('error********')
        print(open_url)
        resp = requests.get(open_url).json()
        chrome_driver = resp["data"]["webdriver"]
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])

    # 直播间链接（队列，循环）
    for i in range(each_group_studio_num):
        studio_url = studio_url_queue.get()
        if (is_dynamic):
            #开启动态抓取
            studio_url_queue=get_url(studio_url, studio_url_queue)
        current_comments_num = []  # list当前评论数量
        driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        # 全局隐式等待
        # driver.implicitly_wait(5)

        driver.get(studio_url)
        print('opening '+str(studio_url))

        #从list随机抽取评论
        comments=random.sample(comments, comment_num)
        #发送若干条评论
        count=0
        ended=False
        retry=0
        # 判断是否下播
        while(ended != True):
            if retry < 5:
                driver.implicitly_wait(5)
                try:
                    retry += 1
                    driver.find_element(By.CLASS_NAME, "live-end-title1")
                    ended=True
                except:
                    print(ads_id+"查找重试"+str(retry)+"次")
            else:
                print(ads_id+"查找等待时间过长，退出")
                break
        if (ended == True):
            print("下播了")
        else:
            print("在直播，开始发送评论")
            for i in range(comment_num):
                print(ads_id + "已评论" + str(count) + "次")
                comm = driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-ltr")
                comm.send_keys(comments[i])
                driver.find_element(By.CLASS_NAME, "webcast-chatroom__comment-post").click()
                count+=1 #发送成功一次
                #等待后进行下一次发送
                time.sleep(comment_interval)
                # driver.quit()
                # requests.get(close_url)
        current_comments_num.append(count)
        time.sleep(2)
    print("直播间已评论完")
    return current_comments_num

def get_url(studio_url,studio_url_queue):
    return studio_url_queue
#返回一个二维列表
def split_groups(ads_id,each_group_num):
    splited_groups=[]
    for i in range(0, len(ads_id), each_group_num):
        splited_groups.append(ads_id[i:i + each_group_num])
    return splited_groups


def manage(group, comments, studio_url_queue, is_dynamic,comment_num,comment_interval,each_group_studio_num):
    list=[]
    for ads_id in group:
        time.sleep(random.randint(1, 5)/10)
        task = pool.submit(start_task, ads_id, comments, studio_url_queue, is_dynamic,comment_num,comment_interval,each_group_studio_num)
        print(threading.current_thread(),task.done())
        list.append(task)
    for task in list:
        task.result()
    return 0
#start_task('i13ovhc','https://www.tiktok.com/@witchlightoracle/live?lang=en','bbbbbbbbb')