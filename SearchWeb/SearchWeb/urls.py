"""SearchWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import include
from django.urls import path

from web.views import Search
from web.views import ReadDB
from web.views import Dashboard
from web.views import get_csrf
from web.views import GetBatchCsv
from web.views import GetMutualState
from web.views import GetBanInDB
from web.views import insertBanInDB
from web.views import deleteBanInDB
from web.views import getURLQueue
from web.views import deleteBanInDB
from web.views import getFailURL
from web.views import getFilter
from web.views import deleteFilter
from web.views import insertFilter
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', include('web.urls')),
    path('readDB/', ReadDB),
    path('dashboard/', Dashboard),
    path('getcsrf/', get_csrf),
    path('dashboard/getbatchcsv/', GetBatchCsv),
    path('dashboard/getMutualState/', GetMutualState),
    path('dashboard/getbanindb/', GetBanInDB),
    path('dashboard/insertbanindb/', insertBanInDB),
    path('dashboard/deletebanindb/', deleteBanInDB),
    path('dashboard/geturlqueue/', getURLQueue),
    path('dashboard/getfailurl/', getFailURL),
    path('dashboard/getfilter/', getFilter),
    path('dashboard/deletefilter/', deleteFilter),
    path('dashboard/insertfilter/', insertFilter),

    
    path('', RedirectView.as_view(url='/search/'))
]
