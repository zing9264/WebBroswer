from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from datetime import datetime

import pandas as pd
import csv

def Search(request):
    return render(request, 'index.html')

def Page(request, searchText, page):
	return render(request, 'index.html', {
        'searchText': searchText,
        'page': page
    })

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

