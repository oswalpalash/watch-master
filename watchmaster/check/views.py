from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.template.loader import render_to_string
# Create your views here.
from django.http import HttpResponse
from subordinates.models import subordinate
import urllib2,subprocess,json
from .models import ping_db,monitor_db

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
	rendered = render_to_string('production/index.html')
	return HttpResponse(rendered)

def send_load_request(hostname,target):                                                       
        subordinate_active=subordinate.objects.get(subordinate_hostname=hostname).subordinate_ip                       
	path="http://"+str(subordinate_active)+"/load?target="+target 
        try:
		content = urllib2.urlopen(path).read()
	except:
		content=""
		pass
        return content

def send_stress_request(hostname,target):
	subordinate_active=subordinate.objects.get(subordinate_hostname=hostname)
	try:
		content = urllib2.urlopen("http://"+subordinate_active.subordinate_ip+"/max_conn?target="+target).read()
	except:
		content=""
		pass
	return content

def send_ping_request(hostname,target):
	subordinate_active=subordinate.objects.get(subordinate_hostname=hostname)
	try:
		content = urllib2.urlopen("http://"+subordinate_active.subordinate_ip+"/ping?target="+target).read()
	except:
		content=""
		pass
	return content

def send_ping(request):
	hostname=request.GET.get('host')
	target=request.GET.get('target')
	ping_reply = []
	if hostname is None:
		all_subordinates = subordinate.objects.all()
		json_obj = {}
		for subordinatee in all_subordinates:
			subordinate_says=send_ping_request(subordinatee.subordinate_hostname,target)
			json_obj[host_to_loc(subordinatee.subordinate_hostname)]=subordinate_says
			add_ping_log(target,subordinatee.subordinate_location,subordinate_says)
		ping_reply=json.dumps(json_obj)

	else:
		subordinate_says=send_ping_request(hostname,target)
		ping_reply.append(subordinate_says)
		subordinate_loc=subordinate.objects.get(subordinate_hostname=hostname).subordinate_location
		add_ping_log(target,subordinate_loc,subordinate_says)
	return HttpResponse(ping_reply)


def test_ping(request):
	hostname=request.GET.get('host')
        target=request.GET.get('target')
	ping_reply = []

	return HttpResponse("test1")
	
def get_ping_logs(hostname,target):
	subordinate_active=subordinate.objects.get(subordinate_hostname=hostname)
        try:
		content = urllib2.urlopen("http://"+subordinate_active+"/get_logs?target="+target).read()
	except:
		content=""
		pass
        return content
def pingOk(sHost):
    try:
        output = subprocess.check_output("ping -c 2 "+sHost, shell=True)
    except Exception, e:
        return False
    return output

def host_to_loc(hostname):
	return subordinate.objects.get(subordinate_hostname=hostname).subordinate_location
def ping_plot(request):
	target=request.GET.get('target')
	subordinates_all=subordinate.objects.all()
	content={}
	for hosts in subordinates_all:
		content[host_to_loc(hosts.subordinate_location)]=get_ping_logs(hosts.subordinate_hostname,target)
	final=json.dumps(content)
	return HttpResponse(final)

def plot(request):
	target=request.GET.get('target')
	all_logs=ping_db.objects.filter(target=target)
	content = {}
	json_obj = {}
	count=0
	for log in all_logs:
		json_obj['result']=str(log.result)
		json_obj['location']=str(log.subordinate_hostname)
		json_obj['timestamp']=str(log.timestamp)
		content[count]=json.dumps(json_obj)
		count = count + 1
	return HttpResponse(json.dumps(content))

def add_ping_log(target,hostname,respo):
	#check and filter if hostname and then convert it to location
	if respo!="":
        	try:
			subordinate_ob = subordinate.objects.get(subordinate_hostname=hostname)
			location =subordinate_ob.subordinate_location
			ping= ping_db(target=target,subordinate_hostname=location,result=respo)
		except:
			ping= ping_db(target=target,subordinate_hostname=hostname,result=respo)
        	ping.save()


def check_loading_time(request):
	target=request.GET.get('target')
	resp=[]
	json_obj={}
	all_subordinates=subordinate.objects.all()
	for subordinate_active in all_subordinates:
		reply=send_load_request(subordinate_active.subordinate_hostname,target)	
		resp.append(reply)
		json_obj[subordinate_active.subordinate_location]=reply
	#resp=send_load_request("mesos-subordinate1",target)
	return HttpResponse(json.dumps(json_obj))

def stress_test(request):
	target=request.GET.get('target')
	resp=[] 
	json_obj={}
	all_subordinates=subordinate.objects.all()
	for subordinate_active in all_subordinates:
		reply=send_stress_request(subordinate_active.subordinate_hostname,target)
		resp.append(reply)
		json_obj[subordinate_active.subordinate_location]=reply
	return HttpResponse(json.dumps(json_obj))
