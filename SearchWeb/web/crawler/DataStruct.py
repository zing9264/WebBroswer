class fetchData():
    def __init__(self,time,status_code,url,ip='0.0.0.0',title='',content='',fetchCount=0):
        self.time = time
        self.status_code = status_code
        self.url = url
        self.ip = ip
        self.title=title
        self.content = content
        self.fetchCount = fetchCount
