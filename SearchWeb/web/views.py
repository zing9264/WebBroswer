from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from datetime import datetime

import pandas as pd
import csv
import json
from .crawlermanage import crawlermanage
from .crawler.DatabaseCtrl import mutual_stateDBinsert
from .crawler.DatabaseCtrl import currentBatchGet

def Search(request):
    return render(request, 'index.html')

def Dashboard(request):
    if 'newthread-URL' in request.POST:
        print("url:" + request.POST['newthread-URL'])
        print("level:" + request.POST['newthread-level'])
        print("wait:" + request.POST['newthread-wait'])
        print("num:" + request.POST['newthread-num'])
        print("state:" + request.POST['newthread-state'])
        datas = [request.POST['newthread-num'], request.POST['newthread-state'], request.POST['newthread-URL'], request.POST['newthread-URL'], request.POST['newthread-level'], request.POST['newthread-wait']]
        #mutual_stateDBinsert(datas)
        return render(request, 'dashboard.html')
    else:
        return render(request, 'dashboard.html')

def Page(request, searchText, page):
	return render(request, 'index.html', {
        'searchText': searchText,
        'page': page
    })

def GetBatchCsv(request):
	
    with open('web\crawler\currentBatch.csv','r', newline='',encoding="utf-8") as fp:
        all_lines = fp.readlines()
    print(all_lines)
    return HttpResponse(all_lines, content_type="text/csv")

def ReadDB(request):
	contentDB = pd.read_csv('web\crawler\contentDB.csv',index_col=0)
	print(contentDB)

	for row in contentDB.iterrows():
		print(row[1].URL)
		print(row[1].content)
		print(row[1].title)

	return render(request, 'null.html', {
        'data': contentDB,
    })

from django.template.context_processors import csrf
from django.http import JsonResponse

def get_csrf(request):
        #生成 csrf 数据，发送给前端
    x = csrf(request)
    csrf_token = x['csrf_token']
    data = {
        'csrf_token': str(csrf_token),
    }
    return JsonResponse(data)
