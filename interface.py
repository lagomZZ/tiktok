import requests,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import math

# 直播间链接（队列，循环）
studio_url = "https://www.tiktok.com/@simply1sue/live?lang=en"
def start_task(ads_id,comments,studio_url,studio_url_queue,is_dynamic):
    # 操控浏览器
    open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + ads_id
    close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + ads_id
    #studio_url=studio_url_queue.get()
    resp = requests.get(open_url).json()
    chrome_driver = resp["data"]["webdriver"]
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)
    print(driver.title)
    if (is_dynamic):
        #开启动态抓取
        driver.get(studio_url)
    time.sleep(10)
    current_comments_num = 0  # 当前评论数量
    #抓取其他url
    get_url(studio_url, studio_url_queue)
    is_disabled = driver.find_element(By.CLASS_NAME, "webcast-chatroom__comment-wrap")
    if (is_disabled.value_of_css_property('cursor') != 'not-allowed'):
        print('go on')
        comm = driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-ltr")
        comm.send_keys(comments)
        time.sleep(10)
        driver.find_element(By.CLASS_NAME, "webcast-chatroom__comment-post").click()
        current_comments_num+=1 #发送成功一次
        time.sleep(10)
        # driver.quit()z
        # requests.get(close_url)
        return current_comments_num

def get_url(studio_url,studio_url_queue):
    return 0

def split_groups(total_num,each_group_num):
    return 0

def get_groups_num(total_num,each_group_num):
    return math.ceil(total_num/each_group_num)

def manage():

    return 0
start_task('i13ovhc','https://www.tiktok.com/@witchlightoracle/live?lang=en','bbbbbbbbb')