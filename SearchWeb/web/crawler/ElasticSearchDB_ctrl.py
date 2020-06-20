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
        #print(x)
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
        #print(x.text)
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
        #print(x.text)
        return (x)

    def CheckDBUrl(self, querystr):
        url = 'http://' + self.serverIP + '/sitedb/_search'
        headers = {'Content-Type': 'application/json'}
        db = {
            "sort" : [
                { "fetchCount" : {"order" : "desc"}},
            ],
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
        #print(url)
        x = requests.get(url, headers=headers)
        a = x.json()
        res = DataStruct.fetchData(a['_source']['lastFetchTime'],200,
        a['_source']['URL'],
        a['_source']['ip_addr'],
        a['_source']['title'],
        a['_source']['content'],
        a['_source']['fetchCount'])
        return res
    

    def updatefetchCountDB(self, ID):
        url = 'http://' + self.serverIP + '/sitedb/_update/'+ID
        headers = {'Content-Type': 'application/json'}
        db = {
            "script": {"source": "ctx._source.fetchCount += 1"}
        }
        x = requests.post(url, headers=headers, data=json.dumps(db))

        return x


class Elasticsearch_IPDB():
    def __init__(self, serverIP='127.0.0.1:9200'):
        self.serverIP = serverIP
    def deleteDB(self):
        url = 'http://'+self.serverIP+'/ipdb'
        x = requests.delete(url)
        print(x.json())
        return (x)

    def newIPDB(self):
        url = 'http://' + self.serverIP + '/ipdb'
        headers = {'Content-Type': 'application/json'}
        db = {
            "mappings": {
                "properties": {
                    "ip_addr": {
                        "type": "keyword"
                    },
                    "URL": {
                        "type": "text"
                    },
                    "fetchCount": {
                        "type": "integer",
                    },
                    "beConnectURL": {
                        "type": "text",
                    },
                    "beConnectCount": {
                        "type": "integer",
                    },
                    "isban": {
                        "type": "integer"
                    },
                    "speed":{
                        "type": "float"
                    },
                    "for_fetch":{
                        "type": "text",
                    }
                }
            }
        }
        x = requests.put(url, headers=headers, data=json.dumps(db))
        print(x.json())
        return (x)

    def insertDataToDB(self, data):
        url = 'http://' + self.serverIP + '/ipdb/_doc/'
        headers = {'Content-Type': 'application/json'}
        db = {
            "ip_addr": data.ip,
            "URL": data.url,
            "speed": data.speed,
            "isban": data.isban,
            "fetchCount": 1,
            "beConnectedURL": data.parentUrl,
            "beConnectedCount": 1,
            "for_fetch":'1'
            }
        x = requests.post(url, headers=headers, data=json.dumps(db))
        #print(x.text)
        return (x)

    def CheckIPinDB(self, querystr):
        url = 'http://' + self.serverIP + '/ipdb/_search'
        headers = {'Content-Type': 'application/json'}
        db = {
            "query": {
                "term": {"ip_addr": querystr}
                }
            }
        x = requests.get(url, headers=headers, data=json.dumps(db))
        
        a = x.json()

        #print(a)
        if (a['hits']['total']['value'] == 0):
            return "NotInIPDB"
        else:
            return a['hits']['hits'][0]['_id']
    
    def getIDdata(self, ID):
        url = 'http://' + self.serverIP + '/ipdb/_doc/'+ID
        headers = {'Content-Type': 'application/json'}
        x = requests.get(url, headers=headers)
        a = x.json()
        res = DataStruct.IPData(ip=a['_source']['ip_addr'],
        url=a['_source']['URL'],
        speed=a['_source']['speed'],
        isban=a['_source']['isban'],
        fetchCount=a['_source']['fetchCount'],
        parentUrl=a['_source']['beConnectedURL'],
        beConnectedCount=a['_source']['beConnectedCount'])
        return res

    def updateDB(self, ID,data):
        url = 'http://' + self.serverIP + '/ipdb/_update/' + ID
        #print(url)
        headers = {'Content-Type': 'application/json'}
        db1 = {
            "script": {"source": "ctx._source.fetchCount += 1"},
        }
        db2 = {
            'doc': {
            "speed": data.speed,
            "ip_addr": data.ip,
            "isban": data.isban,
            }
        }
        db3 = {
            "script": {"source": "ctx._source.URL += ','+(params.URL)",
            "params" : {
            "URL" : data.url}},
        }
        #print(db2)
        x = requests.post(url, headers=headers, data=json.dumps(db1))
        x = requests.post(url, headers=headers, data=json.dumps(db2))
        x = requests.post(url, headers=headers, data=json.dumps(db3))
        #print(x.json())
        return x

    def banInDB(self):
        url = 'http://' + self.serverIP + '/ipdb/_search'
        headers = {'Content-Type': 'application/json'}
        db = {
            "query": {
                "match": {
                    "isban": 1
                }
            }
        }
        x = requests.get(url, headers=headers, data=json.dumps(db))
        
        a = x.json()
        #print(a)
        if (a['hits']['total']['value'] == 0):
            return "noBan"
        else:
            banIPSet=[]
            for i in range(int(len(a['hits']['hits']))):
                #print(i)
                banIPSet.append(a['hits']['hits'][i]['_source']['ip_addr'])
            return banIPSet

    def updateDBisban(self, ID,data):
        url = 'http://' + self.serverIP + '/ipdb/_update/' + ID
        #print(url)
        headers = {'Content-Type': 'application/json'}
        db2 = {
            'doc': {
            "isban": data.isban,
            }
        }
        #print(db2)
        x = requests.post(url, headers=headers, data=json.dumps(db2))
        #print(x.json())
        return x

    def updateDBBeConnectedCnt(self, ID, data):
        url = 'http://' + self.serverIP + '/ipdb/_update/' + ID
        #print(url)
        headers = {'Content-Type': 'application/json'}
        db2 = {
            "script": {"source": "ctx._source.beConnectedCount += 1"},
        }
        #print(db2)
        x = requests.post(url, headers=headers, data=json.dumps(db2))
        #print(x.json())
        db3 = {
            "script": {"source": "ctx._source.parentUrl += ','+(params.URL)",
            "params" : {
            "URL" : data.url}},
        }
        return x


    def getAllData(self):
        url = 'http://' + self.serverIP + '/ipdb/_search'
        headers = {'Content-Type': 'application/json'}
        db = {
            "sort" : [
                { "beConnectedCount" : {"order" : "desc"}},
            ],
            'size':100,
            "query": {
                "match": {
                    "for_fetch": "1"
                }
            }
        }
        x = requests.get(url, headers=headers, data=json.dumps(db))
        a = x.json()
        #print(a)
        if (a['hits']['total']['value'] == 0):
            return "noData"
        else:
            return a
