from concurrent.futures import ThreadPoolExecutor
from random import random

import requests,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

pool = ThreadPoolExecutor(max_workers=5)

def start_task(ads_id,comments,studio_url_queue,is_dynamic,comment_num,comment_interval,each_group_studio_num):
    # 操控浏览器
    open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + ads_id
    close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + ads_id
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
        #判断是否下播
        driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        driver.get(studio_url)
        time.sleep(10)
        is_disabled = driver.find_element(By.CLASS_NAME, "webcast-chatroom__comment-wrap")
        #从list随机抽取评论
        comments=random.sample(comments, comment_num)
        #发送若干条评论
        count=0
        for i in range(comment_num):
            if (is_disabled.value_of_css_property('cursor') != 'not-allowed'):
                print('go on')
                comm = driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-ltr")
                comm.send_keys(comments[i])
                driver.find_element(By.CLASS_NAME, "webcast-chatroom__comment-post").click()
                count+=1 #发送成功一次
                #等待后进行下一次发送
                time.sleep(comment_interval)
                # driver.quit()
                # requests.get(close_url)
        current_comments_num.append(count)
    return current_comments_num

def get_url(studio_url,studio_url_queue):

    return studio_url_queue
#返回一个二维列表
def split_groups(ads_id,each_group_num):
    splited_groups=[]
    for i in range(0, len(ads_id), each_group_num):
        splited_groups.append(ads_id[i:i + each_group_num])
    return splited_groups


def manage(group, comments, studio_url_queue, is_dynamic,comment_num,comment_interval):
    list=[]
    for ads_id in group:
        task = pool.submit(start_task(), ads_id, comments, studio_url_queue, is_dynamic,comment_num,comment_interval)
        list.append(task)
    for task in list:
        task.result()
    return 0
#start_task('i13ovhc','https://www.tiktok.com/@witchlightoracle/live?lang=en','bbbbbbbbb')