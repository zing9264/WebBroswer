import DataStruct
import requests
import json


class Elasticsearch_siteDB():
    def __init__(self, serverIP='127.0.0.1:9200'):
        self.serverIP = serverIP

    def deleteDB(self):
        url = 'http://'+self.serverIP+'/sitedb'
        x = requests.delete(url)
        print(x)
        return (x)

    def newSiteDB(self):
        url = 'http://' + self.serverIP + '/sitedb'
        headers = {'Content-Type': 'application/json'}
        db = {
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_max_word"
                    },
                    "ip_addr": {
                        "type": "ip"
                    },
                    "URL": {
                        "type": "keyword"
                    },
                    "content": {
                        "type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_max_word"
                    },
                    "fetchCount": {
                        "type": "integer"
                    },
                    "lastFetchTime": {
                        "type": "date", "format": "yyyy-MM-dd HH:mm:ss"
                    }
                }
            }
        }
        x = requests.put(url, headers=headers, data=json.dumps(db))
        print(x)
        return (x)

    def insertDataToDB(self, data):
        url = 'http://' + self.serverIP + '/sitedb/_doc/'
        headers = {'Content-Type': 'application/json'}
        db = {
            "title": data.title,
            "ip_addr": data.ip,
            "URL": data.url,
            "content": data.content,
            "lastFetchTime": data.time,
            "fetchCount": 1
            }

        x = requests.post(url, headers=headers, data=json.dumps(db))
        print(x.text)
        return (x)
    


    def searchDB(self, querystr):
        url = 'http://' + self.serverIP + '/sitedb/_search'
        headers = {'Content-Type': 'application/json'}
        db = {
            "query": {"multi_match": {"query": querystr,
                                      "fields": ["title", "content", "URL"],
                                      "analyzer": "ik_max_word"
                                      }
                      },
            "size": 1000,
            "from": 0,
            "highlight": {
                "fields": {
                    "title": {},
                    "content": {},
                    "URL": {}
                }
            }
        }
        x = requests.get(url, headers=headers, data=json.dumps(db))
        print(x.text)
        return (x)

    def CheckDBUrl(self, querystr):
        url = 'http://' + self.serverIP + '/sitedb/_search'
        headers = {'Content-Type': 'application/json'}
        db = {
            "query": {
                "term": {"URL": querystr}
                }
            }
        x = requests.get(url, headers=headers, data=json.dumps(db))
        a = x.json()
        if (a['hits']['total']['value'] == 0):
            return "NotInDB"
        else:
            return a['hits']['hits'][0]['_id']
    
    def getIDdata(self, ID):
        url = 'http://' + self.serverIP + '/sitedb/_doc/'+ID
        headers = {'Content-Type': 'application/json'}
        print(url)
        x = requests.get(url, headers=headers)
        a = x.json()
        res = DataStruct.fetchData(a['_source']['lastFetchTime'],000,
        a['_source']['URL'],
        a['_source']['ip_addr'],
        a['_source']['title'],
        a['_source']['content'],
        a['_source']['fetchCount'])
        return res
    

    def updateDB(self, ID,data):
        url = 'http://' + self.serverIP + '/sitedb/_update/'+ID
        headers = {'Content-Type': 'application/json'}
        db = {
            "script": {"source": "ctx._source.fetchCount += 1"},
            "title": data.title,
            "ip_addr": data.ip,
            "URL": data.url,
            "content": data.content,
            "lastFetchTime": data.time,
        }
        x = requests.post(url, headers=headers, data=json.dumps(db))
        return x
