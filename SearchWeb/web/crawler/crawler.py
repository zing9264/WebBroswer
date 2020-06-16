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
import sys

from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.parse import urldefrag
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
#coding=utf-8


import datetime
ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
import logging
import DataStruct
import ElasticSearchDB_ctrl as dbc
siteDB = dbc.Elasticsearch_siteDB()
ipDB = dbc.Elasticsearch_IPDB()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[logging.FileHandler('error.log', 'w', 'utf-8'),])

logging.debug('Hello debug!')
logging.info('Hello info!')
logging.warning('Hello warning!')
logging.error('Hello error!')
logging.critical('Hello critical!')

maxarray = 10000000
Urlqueue = Queue(maxarray)

def DomaintoIp(url):
    res = urlparse(url)
    try:
        ip=socket.getaddrinfo(res.netloc, res.port, proto=socket.SOL_TCP)[0][4][0]
    except:
        print("dns2ip:Error")
        ip='0.0.0.0'
    return ip

import random


def fetcher(url="https://www.ccu.edu.tw/", speed=0.3):
    
    speed = speed + random.randint(-400, 400) / 1000
    if (speed < 0):
        speed=0
    time.sleep(speed)
    #1.向伺服器傳送get請求
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    try:
        response = requests.get(url, timeout=3, verify=False)
        print('success')
    except requests.exceptions.RequestException as e:
        print(e)
        return DataStruct.fetchData(time=theTime,status_code=504,url=url)

    #checkinDB() 
    #time.sleep(1)
    ip = DomaintoIp(response.url)
        
    #2.使用response處理伺服器的響應內容
    if (response.status_code != 200):
        print("response.status_code :" + str(response.status_code))
        resultData = DataStruct.fetchData(time=theTime,status_code=response.status_code, url=response.url, ip=ip)
        return resultData

    if ('text/html' not in response.headers['Content-Type']):
        resultData = DataStruct.fetchData(time=theTime, status_code=77777, url=response.url, ip=ip, content=response.headers['Content-Type'])
        return resultData
    
    '''
    print("----Fetch Data Detail-----")
    print("Fetch Time :"+theTime)
    print("response.status_code :"+ str(response.status_code))
    print("response.url :" + str(response.url))
    print("IP:" + str(ip))
    '''
    resultData = DataStruct.fetchData(time=theTime, status_code=response.status_code, url=response.url, ip=ip, content=response.text)

    return resultData

SeenDB = DBCtrl.loadSeenDB()

def UrlQueueFilter(url, currentUrl, filterArr):
    newlist = sum(filterArr, [])
    global SeenDB
    isseen, SeenDB, k = DBCtrl.checkinSeenDB(url, SeenDB)
    if (isseen==1):
        return False

    for filterItem in newlist:
        if (filterItem in url):
            return False
    if ('https://' in url):
        pass
    else:
        url = urljoin(currentUrl, url)
    newurl, dummy_frag = urldefrag(url)

    return newurl

def insertDB(url,data):
    checkID=siteDB.CheckDBUrl(url)
    if (checkID != "NotInDB"):
        siteDB.updateDB(checkID, data)
    else:
        siteDB.insertDataToDB(data)
    return 0

def saveQueue(inputthread):
    global SeenDB
    tmpqueue = Queue(maxarray)
    urlqueueDB = []
    i=0
    while (Urlqueue.empty() == False):
        i=i+1
        item = Urlqueue.get()
        urlqueueDB.append(item)
        tmpqueue.put(item)
        if (i % 25000 == 0):
            DBCtrl.urlqueueDBinsert(urlqueueDB, inputthread)
            urlqueueDB = []
    DBCtrl.urlqueueDBinsert(urlqueueDB,inputthread)
    DBCtrl.urlqueueDBdelete(inputthread)
    DBCtrl.updateSeenDB(SeenDB)




def loadQueue(inputthread):
    urlqueueDB =DBCtrl.urlqueueDBget(inputthread)
    for i in urlqueueDB:
        Urlqueue.put(i)

def currentBatchInit(inputurl,inputspeed,inputthread):
#IP,當前網址,當前深度,已爬取,剩餘佇列,失敗數,成功數,重複URL數,速率,經過時間
    tmpBatch = DBCtrl.currentBatchGet(inputthread)
    ip = DomaintoIp(inputurl)
    currentBatch = DataStruct.currentBatch(ip, inputurl, tmpBatch[2], tmpBatch[3], tmpBatch[4], tmpBatch[5], tmpBatch[6], tmpBatch[7], inputspeed, tmpBatch[9])
    time.sleep(5)
    #ip='0.0.0.0',url='',level=0,totalFetchCnt=0,queueCnt=0,failCnt=0,successCnt=0,redundancyUrlCnt=0,speed=0.05,passedTime=0
    return currentBatch

def isBan(inputurl):
    ip = DomaintoIp(inputurl)
    IDcheck = ipDB.CheckIPinDB(ip)
    if (IDcheck == "NotInIPDB"):
        return False
    else:
        if (int(ipDB.getIDdata(IDcheck).isban) == 0):
            return False
        else:
            return True



def startFetch(inputurl='https://www.ccu.edu.tw/', inputLevel=6,inputspeed=0.05,inputthread=1):

    currentBatch = currentBatchInit(inputurl,inputspeed,inputthread)
    startTime = time.time()
    saveTime=0
    passTime = currentBatch.passedTime
    filterArr=DBCtrl.filterArrGet()
    loadQueue(inputthread)                 #讀取佇列
    if (Urlqueue.empty() == True):#若空則由種子網站開始
        Urlqueue.put([inputurl, 0])
    fetchCnt =currentBatch.totalFetchCnt 
    while (Urlqueue.empty() == False):#爬取到佇列空為止
        item = Urlqueue.get()
        currentUrl = item[0]
        currentLevel = item[1]
        print("currentUrl=" + str(currentUrl))
        print("currentLevel=" + str(currentLevel))
        if (int(currentLevel) >= int(inputLevel)):# 超過預定深度就不爬取
            continue
        if isBan(currentUrl):
            continue
        urlIDcheck = siteDB.CheckDBUrl(currentUrl)# 檢查是否存在資料庫
        if (urlIDcheck == 'NotInDB'):  # 若不存在則進行爬取
            fetchCnt=fetchCnt+1
            print('NotInDB')
            fetchData = fetcher(currentUrl,currentBatch.speed) #執行FETCHER 回傳fetchData的資料型態 定義在DataStruct.py
            if (fetchData.status_code != 200): #檢查碼是否正常
                currentBatch.failCnt=currentBatch.failCnt+1
                continue
            currentBatch.successCnt=currentBatch.successCnt+1
            fetchData.title, contextpool, links = ps.parser(fetchData.content)#將爬取到的資料丟進PARSER，取得標題、連結、內文
            fetchData.content = "".join(contextpool)#將內文從ARRAY合併成一個字串
            insertDB(currentUrl, fetchData)#送到ELASTIC DB
            links.sort()
            #print(links)
            for i in links:  #將連結加到QUEUE
                tmpUrl = UrlQueueFilter(i,currentUrl,filterArr)
                if (tmpUrl == False):
                    continue
                Urlqueue.put([tmpUrl, str(int(currentLevel) + 1)])

            IPData = DataStruct.IPData(ip=fetchData.ip, url=currentUrl, fetchCount=1, isban=0, speed=inputspeed)
            ipID = ipDB.CheckIPinDB(IPData.ip)
            if (ipID != 'NotInIPDB'):
                ipDB.updateDB(ipID, IPData)
            else:
                ipDB.insertDataToDB(IPData)

        else: #若該筆連結已存在資料庫中，更新他被爬取過的次數(記錄被多少網站連過)，這裡沒有對內容更新，若要更新內容，需要再寫一個針對資料庫已有資料進行更新的程式。
            print('indb')
            fetchData = siteDB.getIDdata(urlIDcheck)
            insertDB(currentUrl, fetchData)
            currentBatch.redundancyUrlCnt = currentBatch.redundancyUrlCnt + 1  #統計重複的URL總數
        timeLag=time.time()-startTime
        saveTime = saveTime+ timeLag
        passTime = passTime +timeLag
        startTime = time.time()
        if (saveTime >= 4):  #對網頁要顯示的資料進行更新
            saveTime=0
            currentBatchData = [fetchData.ip,fetchData.url,currentLevel,fetchCnt,Urlqueue.qsize(),currentBatch.failCnt,currentBatch.successCnt,currentBatch.redundancyUrlCnt,currentBatch.speed,passTime] #IP,當前網址,當前深度,已爬取,剩餘佇列,失敗數,成功數,重複URL數,速率,經過時間
            DBCtrl.currentBatchInsert(currentBatchData, inputthread)
            filterArr=DBCtrl.filterArrGet()

        if (fetchCnt % 250 == 0): #自動存檔功能
            print('----------SaveData--------')
            saveQueue(inputthread)
            loadQueue(inputthread)


    print('----------finish--------')
    saveQueue(inputthread)
    

if __name__ == "__main__":
    startFetch(inputurl=sys.argv[1],inputLevel=sys.argv[2],inputthread=sys.argv[3],inputspeed=sys.argv[4])
