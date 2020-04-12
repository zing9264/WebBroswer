import DataStruct 
import requests
import json

class Elasticsearch_siteDB():
    def __init__(self, serverIP='127.0.0.1:9200'):
        self.serverIP = serverIP
        
    def deleteDB(self):
        url='http://'+self.serverIP+'/sitedb'
        x = requests.delete(url)
        print(x)
        return (x)

    def newSiteDB(self):
        url = 'http://' + self.serverIP + '/sitedb'
        headers = {'Content-Type': 'application/json'}
        db={"mappings": {"properties":{"title":{ "type": "text","analyzer": "ik_max_word", "search_analyzer": "ik_max_word"},  "ip_addr":{ "type": "ip"},  "URL":{ "type": "text","analyzer": "ik_max_word", "search_analyzer": "ik_max_word"}, "content":{ "type": "text","analyzer": "ik_max_word", "search_analyzer": "ik_max_word"}, "lastFetchTime":{ "type": "date","format": "yyyy-MM-dd HH:mm:ss"}}}}
        x = requests.put(url,headers=headers, data=json.dumps(db))
        print(x)
        return (x)
        
    def insertDataToDB(self, data):
        url = 'http://' + self.serverIP + '/sitedb/_doc/'
        headers = {'Content-Type': 'application/json'}

        db = {"title": data.title,
        "ip_addr": data.ip,
        "URL": data.url,
        "content": data.content,
        "lastFetchTime": data.time
        }
        x = requests.post(url,headers=headers, data=json.dumps(db))
        print(x.text)
        return (x)
'''

    def checkUrlInDB():

    
    

POST  /sitedb/_doc/
{ 
  "title":"國立中正大學　National Chung Cheng University",
  "ip_addr":"140.123.5.6",
  "URL":"https://www.ccu.edu.tw/",
  "content":"保證責任台灣農業合作社聯合社檢送「第98屆國際合作社節合作事業微電影徵選及繪畫比賽(含四格漫畫)參賽辦法」乙份，歡迎師生踴躍參加投稿。",
  "lastFetchTime":"2020-04-12 11:29:25"
}

POST  /sitedb/_doc/
{ 
  "title":"國立中正大學　National Chung Cheng University",
  "ip_addr":"140.123.5.6",
  "URL":"https://www.ccu.edu.tw/",
  "content":"這位中正的教授今天一來就在白板上寫作業可以用其他語言寫作業可是他當初自己也說這門課會用到蛇蛇語言(你要說讓不會的同學有其他替代語言方案也不是不行la)可是助教的講義也都編好了，好歹也先跟助教商量一下吧？？？教授之前一開始還說要留最後半小時讓助教帶我們上機好笑的是他把時間交給助教的時候距離下課剩不到幾分鐘。我相信助教當下說自己這樣編心酸已經算口氣很好了，教授也許有自己的立場，但是今天如果換作我是助教真心覺得很不受尊重，尤其教授說助教就是幫忙改作業跟點名的(?)誇張的是最後教授根本不想多做回應，拋下一句不要浪費同學寶貴的時間......我最聽不下去的是他跟助教說不然你來當老師，這句話未免太不負責任...?",
  "lastFetchTime":"2020-04-12 11:29:25"
}

GET /sitedb/_search
{
  "query" : { 
    "multi_match" : { 
      "query": "中正 教授",
      "fields":["title", "content","URL"],
      "analyzer":"ik_max_word"
    }
  },
  "size": 1000,
  "from": 0,
   "highlight" : {
        "fields" : {
            "title" : {},
            "content" : {},
            "URL" : {}
        }
    }
  
}

'''
