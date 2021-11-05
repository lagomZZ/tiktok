from concurrent.futures import ThreadPoolExecutor

from interface import split_groups, get_groups_num, manage
import queue,time,math

'''参数'''
comments=["aaaa","bbbbb"] #话术（list）
ads_id = ["i13ovhc","i13un9b" ] #浏览器id
comment_interval=10 #评论间隔
comment_num=10 #评论数量
total_num=20 #总账号数
each_group_num=5 #单组账号数
similtaneous_groups_num=get_groups_num(total_num,each_group_num) #同时运行分组数

#直播间队列初始化
studio_url_queue=queue.Queue()
for item in ['https://www.tiktok.com/@mysticalempress233/live?lang=en',
'https://www.tiktok.com/@kjbcandle/live?lang=en',
'https://www.tiktok.com/@kingcrio/live?lang=en',
'https://www.tiktok.com/@bigdaddy1123456/live?lang=en'
]:
    studio_url_queue.put(item)

studio_url_queue_num=studio_url_queue.qsize() #直播间队列内数量
each_group_studio_num= math.floor(studio_url_queue_num/similtaneous_groups_num) #每组分配直播间数
splited_groups=split_groups(total_num,each_group_num) #返回的分组嵌套列表
groups_num=len(splited_groups) #组数
loop=groups_num/similtaneous_groups_num #循环数
is_dynamic=False #动态抓取，默认否

'''执行过程'''
#线程池
pool = ThreadPoolExecutor(max_workers=10)

#循环次数
for l in range(loop):
    print('this is '+ l +'round')
    #分组执行,先取出同时运行的组
    similtaneous_groups=splited_groups[l:l+similtaneous_groups_num]
    count=0
    list=[]
    for group in similtaneous_groups:
        #每个组一个线程，然后管理线程，进入同一个直播间
        print('group ' + count + ' start' + time.time())
        count+=1
        studio_url = studio_url_queue.get()
        task = pool.submit(manage,group, comments, studio_url, studio_url_queue, is_dynamic,comment_num,comment_interval)
        list.append(task)
    for task in list:
        task.result()


pool.shutdown(wait=True)