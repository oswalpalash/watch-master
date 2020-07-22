from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import subordinate
from check.models import monitor_db
def index(request):
    all_subordinates=subordinate.objects.all()
    content = []
    for subordinates in all_subordinates:
	content.append(subordinates.subordinate_ip)
	content.append(" "+subordinates.subordinate_hostname)
	content.append(" "+subordinates.subordinate_location+"\n")
	content.append(" "+subordinates.subordinate_location+"<br>") 
    return HttpResponse(content)

def add(request):
    target=request.GET.get('target')
    monitor = monitor_db(target=target,test="ping")
    monitor.save()
    return HttpResponse(True)
