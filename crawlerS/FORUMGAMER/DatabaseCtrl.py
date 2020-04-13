import pandas as pd
import numpy as np
import hashlib
import csv

maxarray = 1000000
def urlqueueDBget():
    urlqueueDB=[]
    with open('urlqueueDB.csv','r', newline='',encoding="utf-8") as csvfile:
    # 讀取 CSV 檔案內容
        reader = csv.reader(csvfile)
        for row in reader:
            urlqueueDB.append(row)
    return urlqueueDB


def urlqueueDBinsert(datas):
    with open('urlqueueDB.csv', 'w', newline='',encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for row in datas:
            writer.writerow(row)
            
'''
def checkinSeenDB(content):
    print("init--------")
    SeenDB=[]
    with open('SeenDB.csv', newline='') as csvfile:
    # 讀取 CSV 檔案內容
        reader = csv.reader(csvfile)
        for row in reader:
            SeenDB.extend(row)
    print("init--------fin")

    md5hash = hashlib.md5()
    md5hash.update(fetchURL.encode("utf-8"))
    md5hash.hexdigest()
    ten = int(md5hash.hexdigest(), 16)
    idx=ten % maxarray
    print("check-----------------")
    if (SeenDB[idx] == '0'):
        SeenDB[idx] = fetchURL
        print("insert the new URL at "+ str(idx))
        return 1,SeenDB,str(idx)
    k=idx
    while SeenDB[k] != fetchURL:
        if (k == idx - 1):
            print('ERROR database is full')
            return -1,SeenDB,str(k)
        if (SeenDB[k] == '0'):
            SeenDB[k] = fetchURL
            print("insert the new URL at "+ str(k))
            return 1,SeenDB,str(k)
        k = k + 1
        print("collision at "+k)
    print(fetchURL + "  collision at " + str(ten % maxarray))
    print("already exists")
    return 0,SeenDB,str(k)

def contentDBget():
    contentDB = pd.read_csv('contentDB.csv',index_col=0)
    print("---get---\n")
    print(contentDB)  
    return contentDB

def contentDBinsert(URL,content,title):
    contentDB = contentDBget()
        # 先創建一個DataFrame，用來增加進數據框的最後一行
    new = pd.DataFrame({'URL': URL,'content':content,'title':title},index=[1])
    print(new)
    print("-------最後一行新增一行------")
    contentDB=contentDB.append(new,ignore_index=True) 
    print(contentDB)
    contentDB.to_csv('contentDB.csv') 

def resetcontentDB():
    global maxarray
    contentDB = ['0'] * maxarray
    contentDB=pd.DataFrame(columns = ["URL", "content",'title'])
    print(contentDB)
    contentDB.to_csv('contentDB.csv') 


def updateSeenDB(SeenDB):
    with open('SeenDB.csv', 'w', newline='') as csvfile:
  # 以空白分隔欄位，建立 CSV 檔寫入器
        writer = csv.writer(csvfile, delimiter=',')
        print("w:")
        writer.writerow(SeenDB)

def resetSeenDB():
    global maxarray
    with open('SeenDB.csv', 'w', newline='') as csvfile:
        seenDB=['0']*maxarray

        writer = csv.writer(csvfile, delimiter=',')
        print("reset")
        writer.writerow(seenDB)

def resetALLDB():
    resetSeenDB()
    resetcontentDB()
if __name__ == "__main__":
    resetALLDB()
    pass
'''
