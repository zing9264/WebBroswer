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
import socket
from urllib.parse import urlparse
import datetime
ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
import logging
import DataStruct
import ElasticSearchDB_ctrl as dbc


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

def DomaintoIp(url):
    res = urlparse(url)
    try:
        ip=socket.getaddrinfo(res.netloc, res.port, proto=socket.SOL_TCP)[0][4][0]
    except:
        print("dns2ip:Error")
    return ip


def fetcher(url="https://www.ccu.edu.tw/"):
    #1.向伺服器傳送get請求
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    response=requests.get(url, timeout = 3)
    #checkinDB() 
    time.sleep(1)

    #2.使用response處理伺服器的響應內容
    if (response.status_code != 200):
        print("response.status_code :"+response.status_code)
        return - 1, response.url

    ip= DomaintoIp(response.url)
    print("----Fetch Data Detail-----")
    print("Fetch Time :"+theTime)
    print("response.status_code :"+ str(response.status_code))
    print("response.url :" + str(response.url))
    print("IP:" + str(ip))
    resultData=DataStruct.fetchData(theTime,response.status_code,response.url,ip,response.text)

    return resultData
    
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
    fetchData = fetcher(currentUrl)
    print('------------------------------')
    print(fetchData.time)
    print(fetchData.status_code)
    print(fetchData.url)
    print(fetchData.ip)
    print(fetchData.content)
    print('------------------------------')
    fetchData.title, contextpool, links = ps.parser(fetchData.content)
    fetchData.content="".join(contextpool)
    siteDB = dbc.Elasticsearch_siteDB()
    siteDB.deleteDB()
    siteDB.newSiteDB()
    siteDB.insertDataToDB(fetchData)
    #SiteDbInsert(fetchData)
    #title, contextpool, links = ps.parser(fetchData.content)
    '''
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
    '''
