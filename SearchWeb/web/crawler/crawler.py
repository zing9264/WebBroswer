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
from urllib.parse import urljoin
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


import datetime
ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
import logging
import DataStruct
import ElasticSearchDB_ctrl as dbc
siteDB = dbc.Elasticsearch_siteDB()

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
Urlqueue = Queue(1000000)

def DomaintoIp(url):
    res = urlparse(url)
    try:
        ip=socket.getaddrinfo(res.netloc, res.port, proto=socket.SOL_TCP)[0][4][0]
    except:
        print("dns2ip:Error")
    return ip


def fetcher(url="https://www.ccu.edu.tw/"):
    time.sleep(1)
    #1.向伺服器傳送get請求
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    response=requests.get(url, timeout = 3, verify=False)
    #checkinDB() 
    time.sleep(1)
    ip= DomaintoIp(response.url)
    #2.使用response處理伺服器的響應內容
    if (response.status_code != 200):
        print("response.status_code :" + str(response.status_code))
        resultData = DataStruct.fetchData(time=theTime,status_code=response.status_code, url=response.url, ip=ip)
        return resultData

    print("----Fetch Data Detail-----")
    print("Fetch Time :"+theTime)
    print("response.status_code :"+ str(response.status_code))
    print("response.url :" + str(response.url))
    print("IP:" + str(ip))
    resultData = DataStruct.fetchData(time=theTime, status_code=response.status_code, url=response.url, ip=ip, content=response.text)
    return resultData
    
def UrlQueueFilter(url, currentUrl):

    if ('mailto:'in url):
        return False
    elif ('None'in url):
        return False
    elif ('.pdf'in url):
        return False
    elif ('https://' in url):
        pass
    else:
        url=urljoin(currentUrl,url)
    newurl = urlparse(url,allow_fragments=False)
    print(newurl)
    return newurl.geturl()

def insertDB(url,data):
    checkID=siteDB.CheckDBUrl(url)
    if (checkID != "NotInDB"):
        siteDB.updateDB(checkID, data)
    else:
        siteDB.insertDataToDB(data)
    return 0

def saveQueue():
    tmpqueue = Queue(1000000)
    urlqueueDB = []
    while (Urlqueue.empty() == False):
        item = Urlqueue.get()
        urlqueueDB.append(item)
        tmpqueue.put(item)
    DBCtrl.urlqueueDBinsert(urlqueueDB)

def loadQueue():
    urlqueueDB =DBCtrl.urlqueueDBget()
    for i in urlqueueDB:
        Urlqueue.put(i)



def startFetch(currentUrl= 'https://www.ccu.edu.tw/'):
    fetchData = fetcher(currentUrl)
    print('------------------------------')
    print(fetchData.time)
    print(fetchData.status_code)
    print(fetchData.url)
    print(fetchData.ip)
    print(fetchData.content)
    print('------------------------------')
    fetchData.title, contextpool, links = ps.parser(fetchData.content)
    fetchData.content = "".join(contextpool)
    insertDB(currentUrl,fetchData)

    #SiteDbInsert(fetchData)
    #title, contextpool, links = ps.parser(fetchData.content)
    links.sort()
    loadQueue()
    for i in links:
        print(i)
        tmpUrl = UrlQueueFilter(i,currentUrl)
        print(tmpUrl)
        if (tmpUrl == False):
            continue
        Urlqueue.put(tmpUrl)
    saveQueue()
    loadQueue()

    while (Urlqueue.empty() == False):
        currentUrl = Urlqueue.get()
        print("currentUrl=" + currentUrl)
        urlIDcheck = siteDB.CheckDBUrl(currentUrl)
        if (urlIDcheck == 'NotInDB'):
            fetchData = fetcher(currentUrl)
            if (fetchData.status_code != 200):
                continue
            fetchData.title, contextpool, links = ps.parser(fetchData.content)
            fetchData.content = "".join(contextpool)
            insertDB(currentUrl, fetchData)
            links.sort()
            for i in links:
                print(i)
                tmpUrl = UrlQueueFilter(i,currentUrl)
                print(tmpUrl)
                if (tmpUrl == False):
                    continue
                Urlqueue.put(tmpUrl)
            saveQueue()
            loadQueue()
        else:
            fetchData = siteDB.getIDdata(urlIDcheck)
            insertDB(currentUrl,fetchData)



if __name__ == "__main__":
    startFetch()
