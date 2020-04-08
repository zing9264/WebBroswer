from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from datetime import datetime

def hello_world(request):
    return render(request, 'index.html', {
        'now': str(datetime.today()),
    })