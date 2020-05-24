from django.template.context_processors import csrf

def get_csrf(request):
        #生成 csrf 数据，发送给前端
    x = csrf(request)
    csrf_token = x['csrf_token']
    return HttpResponse('{} ; {}'.format(str(re), csrf_token))
