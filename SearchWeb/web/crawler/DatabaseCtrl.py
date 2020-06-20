import pandas as pd
import numpy as np
import hashlib
import csv
import os
import glob
import time
Seenmaxarray = 1000000
def urlqueueDBget(threadnum):
        
    urlqueueDBPath = os.path.join(os.path.dirname(__file__), 'urlqueueDB_' + str(threadnum))
    urlqueueDB = []
    with open(glob.glob(urlqueueDBPath+'/*')[0],'r', newline='',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
        reader = csv.reader(csvfile)
        for row in reader:
            urlqueueDB.append(row)
    return urlqueueDB

def urlqueueDBinsert(datas, threadnum):
    urlqueueDBPath = os.path.join(os.path.dirname(__file__), 'urlqueueDB_' + str(threadnum))
    f = os.listdir(urlqueueDBPath)
    name = sorted(f, reverse=True)
    newName = 'Q' + str(threadnum) + '_' + str(int(name[0].replace('Q' + str(threadnum) + '_', '').replace('.csv', ''))+1) + '.csv'
    urlqueueDBPath = os.path.join(os.path.dirname(__file__), 'urlqueueDB_' + str(threadnum) ,newName)
    with open(urlqueueDBPath, 'w', newline='',encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for row in datas:
            writer.writerow(row)

def urlqueueDBdelete(threadnum):
    path = os.path.join(os.path.dirname(__file__), 'urlqueueDB_' + str(threadnum))
    # 獲取該目錄下所有檔案，存入列表中
    f = os.listdir(path)
    # print(len(f))
    # print(f)
    deletepath = os.path.join(os.path.dirname(__file__), 'urlqueueDB_' + str(threadnum),f[0])
    os.remove(deletepath)
    for i in range(len(f)-1):
        # 用os模組中的rename方法對檔案改名
        leftpath = os.path.join(os.path.dirname(__file__), 'urlqueueDB_' + str(threadnum),f[i])
        rigthpath = os.path.join(os.path.dirname(__file__), 'urlqueueDB_' + str(threadnum),f[i+1])
        os.rename(rigthpath,leftpath)
    

def mutual_stateDBget(threadnum):
    urlqueueDB=[]
    with open('mutual_state.csv','r', newline='',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0]==threadnum:
                return row


def mutual_stateDBinsert(datas):
    with open('web\crawler\mutual_state.csv','r', newline='',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
    with open('web\crawler\mutual_state.csv', 'w', newline='',encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        rows[int(datas[0])] = datas
        writer.writerows(rows)
    return

def currentBatchGet(threadnum):
    currentBatchPath = os.path.join(os.path.dirname(__file__), 'currentBatch_'+str(threadnum)+'.csv')

    with open(currentBatchPath,'r', newline='',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
    return rows[1]

def currentBatchInsert(datas,threadnum):
    currentBatchPath = os.path.join(os.path.dirname(__file__), 'currentBatch_'+str(threadnum)+'.csv')

    with open(currentBatchPath,'r', newline='',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
        reader = csv.reader(csvfile)
        # print(reader)
        rows = [row for row in reader]
    with open(currentBatchPath, 'w', newline='',encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # print(rows)
        # print(datas)
        rows[1] = datas
        # print(rows)
        writer.writerows(rows)
    return

def blackListInsert(data):
    with open('black_list.csv', 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    return data

def filterArrGet():
    filter_list_Path = os.path.join(os.path.dirname(__file__), 'filter_list.csv')
    with open(filter_list_Path, 'r', newline='', encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
        reader = csv.reader(csvfile)
        print(reader)
        rows = [row for row in reader]
    return rows

def filterArrInsert(data):
    filter_list_Path = os.path.join(os.path.dirname(__file__), 'filter_list.csv')
    with open(filter_list_Path, 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
    return data

def filterArrDelete(data):
    arr = filterArrGet()
    print(arr)
    for i in range(len(arr)):
        if (arr[i] == data):
            print('find')
            newarr = arr[0:i] +arr[i+1 :]
            print(newarr)
            filter_list_Path = os.path.join(os.path.dirname(__file__), 'filter_list.csv')
            with open(filter_list_Path, 'w', newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(newarr)
            return 0
    return 1

def loadSeenDB(thread):
    print("init--------")
    SeenDB=[]
    with open('SeenDB_'+str(thread)+'.csv', newline='',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
        reader = csv.reader(csvfile)
        for row in reader:
            SeenDB.extend(row)
    print("init--------fin")
    return SeenDB

def checkinSeenDB(fetchURL, SeenDB):
    global Seenmaxarray
    md5hash = hashlib.md5()
    md5hash.update(fetchURL.encode("utf-8"))
    md5hash.hexdigest()
    ten = int(md5hash.hexdigest(), 16)
    idx=ten % Seenmaxarray
    # print("check-----------------")
    if (SeenDB[idx] == '0'):
        SeenDB[idx] = fetchURL
        # print("insert the new URL at "+ str(idx))
        return 0,SeenDB,str(idx)
    k=idx
    while SeenDB[k] != fetchURL:
        if (k == idx - 1):
            print('ERROR database is full')
            return -1,SeenDB,str(k)
        if (SeenDB[k] == '0'):
            SeenDB[k] = fetchURL
            # print("insert the new URL at "+ str(k))
            return 0,SeenDB,str(k)
        k = k + 1
        if k == Seenmaxarray:
            k = 0
        # print("collision at "+str(k))
    # print(fetchURL + "  collision at " + str(ten % Seenmaxarray))
    # print("already exists")
    return 1,SeenDB,str(k)

def updateSeenDB(SeenDB,thread):
    with open('SeenDB_'+str(thread)+'.csv', 'w', newline='', encoding="utf-8") as csvfile:
        # 以空白分隔欄位，建立 CSV 檔寫入器
        writer = csv.writer(csvfile, delimiter=',')
        print("w:")
        writer.writerow(SeenDB)

            

def resetSeenDB(thread):
    global Seenmaxarray
    with open('SeenDB_'+str(thread)+'.csv', 'w', newline='', encoding="utf-8") as csvfile:
        seenDB=['0']*Seenmaxarray
        writer = csv.writer(csvfile, delimiter=',')
        print("reset")
        writer.writerow(seenDB)




def failURLDBget(threadnum):
    failURLDBPath = os.path.join(os.path.dirname(__file__), 'failURLDB_' + str(threadnum)+ '.csv')
    failURLDB = []
    with open(failURLDBPath,'r', newline='',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
        reader = csv.reader(csvfile)
        for row in reader:
            failURLDB.append(row)
    return failURLDB

def failURLDBinsert(datas, threadnum):
    failURLDBPath = os.path.join(os.path.dirname(__file__), 'failURLDB_' + str(threadnum)+ '.csv')
    with open(failURLDBPath, 'a', newline='',encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(datas)

def resetFailURLDB(threadnum):
    failURLDBPath = os.path.join(os.path.dirname(__file__), 'failURLDB_' + str(threadnum)+ '.csv')
    f=open(failURLDBPath, 'w')
    f.write('')

