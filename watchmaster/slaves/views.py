from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import slave
from check.models import monitor_db
def index(request):
    all_slaves=slave.objects.all()
    content = []
    for slaves in all_slaves:
	content.append(slaves.slave_ip)
	content.append(" "+slaves.slave_hostname)
	content.append(" "+slaves.slave_location+"\n")
	content.append(" "+slaves.slave_location+"<br>") 
    return HttpResponse(content)

def add(request):
    target=request.GET.get('target')
    monitor = monitor_db(target=target,test="ping")
    monitor.save()
    return HttpResponse(True)
