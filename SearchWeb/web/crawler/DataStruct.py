class fetchData():
    def __init__(self,time,status_code,url,ip='0.0.0.0',title='',content='',fetchCount=0):
        self.time = time
        self.status_code = status_code
        self.url = url
        self.ip = ip
        self.title=title
        self.content = content
        self.fetchCount = fetchCount

#IP,當前網址,當前深度,已爬取,剩餘佇列,失敗數,成功數,重複URL數,速率,經過時間
class currentBatch():
    def __init__(self,ip='0.0.0.0',url='',level=0,totalFetchCnt=0,queueCnt=0,failCnt=0,successCnt=0,redundancyUrlCnt=0,speed=0.05,passedTime=0):
        self.ip = ip
        self.url = url
        self.level=int(level)
        self.totalFetchCnt = int(totalFetchCnt)
        self.queueCnt = int(queueCnt)
        self.failCnt=int(failCnt)
        self.successCnt = int(successCnt)
        self.redundancyUrlCnt = int(redundancyUrlCnt)
        self.speed = float(speed)
        self.passedTime = float(passedTime)
        

#IP,當前網址,當前深度,已爬取,剩餘佇列,失敗數,成功數,重複URL數,速率,經過時間
class IPData():
    def __init__(self,ip='0.0.0.0',url='test',fetchCount=1,isban=0,speed=0.05,parentUrl='',beConnectedCount=1):
        self.ip = ip
        self.url = url
        self.parentUrl = parentUrl
        self.beConnectedCount=beConnectedCount
        self.fetchCount = int(fetchCount)
        self.isban=int(isban)
        self.speed = float(speed)
