import requests
import pandas as pd
import numpy as np
import hashlib
import csv
from bs4 import BeautifulSoup
import DatabaseCtrl as DBCtrl
import myparser as ps
from queue import Queue
from functools import cmp_to_key
import time

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[logging.FileHandler('error.log', 'w', 'utf-8'),])
                    
logging.debug('Hello debug!')
logging.info('Hello info!')
logging.warning('Hello warning!')
logging.error('Hello error!')
logging.critical('Hello critical!')

maxarray = 1000000
Urlqueue = Queue(10000)

def fetcher(url="https://www.ccu.edu.tw/"):
    #1.向伺服器傳送get請求
    time.sleep(3)
    response=requests.get(url, timeout = 3)
    #2.使用response處理伺服器的響應內容
    if (response.status_code != 200):
        print("response.status_code :"+response.status_code)
        return -1, response.url
        
    print(response.url)
    result,seendb,idx=DBCtrl.checkinSeenDB(response.url) #檢查資料是否存在
    print(result)
    if (result == 0):
        pass
    elif (result == -1):
        pass
    else: #若都沒出現在資料庫中，將其網頁送至HTML的資料庫，待文本分析處理
        with open('htmldb/' + idx + ".html", 'w', encoding=response.encoding, newline='') as f:
            try:
                f.write(response.text)
            except:
                print('寫入網頁發生錯誤')
                logging.error('url:'+response.url)
                logging.error('idx:'+idx)
                logging.error('encoding:'+str(response.encoding))

        DBCtrl.updateSeenDB(seendb)#更新已看過的資料庫
    print("checkfin-------------")
    return idx, response.url
    
def UrlQueueFilter(currentUrl):
    url = Urlqueue.get()
    if ('https://' in url):
        pass
    elif ('mailto:'in url):
        return False
    elif ('None'in url):
        return False
    elif ('/#'in url):
        return False
    elif (url[0] == '/'):
        url = currentUrl + url[1:]
    else:
        url = currentUrl + url
    return url



if __name__ == "__main__":
    currentUrl = 'https://www.ccu.edu.tw/'
    idx, url = fetcher(currentUrl)
    title, contextpool, links = ps.parser(idx)
    print(url)
    print(title)
    print(contextpool)
    DBCtrl.contentDBinsert(url, "[s=p=l=i=t]".join(contextpool), title)
    links.sort()
    for _ in links:
        print(_)
        Urlqueue.put(_)

    while (Urlqueue.empty() == False):
        tmpUrl = UrlQueueFilter(currentUrl)
        print(tmpUrl)

        if (tmpUrl == False):
            continue
        idx, url = fetcher(tmpUrl)
        if (idx == -1):
            continue
        title, contextpool, links = ps.parser(idx)
        DBCtrl.contentDBinsert(url, "[s=p=l=i=t]".join(contextpool), title)


