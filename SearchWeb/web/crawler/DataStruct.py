class fetchData():
    def __init__(self,time,status_code,url,ip,content=''):
        self.time = time
        self.status_code = status_code
        self.url = url
        self.ip = ip
        self.title=''
        self.content = content
