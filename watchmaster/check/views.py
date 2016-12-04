from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.template.loader import render_to_string
# Create your views here.
from django.http import HttpResponse
from slaves.models import slave
import urllib2,subprocess,json
from .models import ping_db,monitor_db

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
	rendered = render_to_string('production/index.html')
	return HttpResponse(rendered)

def send_load_request(hostname,target):                                                       
        slave_active=slave.objects.get(slave_hostname=hostname).slave_ip                       
	path="http://"+str(slave_active)+"/load?target="+target 
        try:
		content = urllib2.urlopen(path).read()
	except:
		content=""
		pass
        return content

def send_stress_request(hostname,target):
	slave_active=slave.objects.get(slave_hostname=hostname)
	try:
		content = urllib2.urlopen("http://"+slave_active.slave_ip+"/max_conn?target="+target).read()
	except:
		content=""
		pass
	return content

def send_ping_request(hostname,target):
	slave_active=slave.objects.get(slave_hostname=hostname)
	try:
		content = urllib2.urlopen("http://"+slave_active.slave_ip+"/ping?target="+target).read()
	except:
		content=""
		pass
	return content

def send_ping(request):
	hostname=request.GET.get('host')
	target=request.GET.get('target')
	ping_reply = []
	if hostname is None:
		all_slaves = slave.objects.all()
		json_obj = {}
		for slavee in all_slaves:
			slave_says=send_ping_request(slavee.slave_hostname,target)
			json_obj[host_to_loc(slavee.slave_hostname)]=slave_says
			add_ping_log(target,slavee.slave_location,slave_says)
		ping_reply=json.dumps(json_obj)

	else:
		slave_says=send_ping_request(hostname,target)
		ping_reply.append(slave_says)
		slave_loc=slave.objects.get(slave_hostname=hostname).slave_location
		add_ping_log(target,slave_loc,slave_says)
	return HttpResponse(ping_reply)


def test_ping(request):
	hostname=request.GET.get('host')
        target=request.GET.get('target')
	ping_reply = []

	return HttpResponse("test1")
	
def get_ping_logs(hostname,target):
	slave_active=slave.objects.get(slave_hostname=hostname)
        try:
		content = urllib2.urlopen("http://"+slave_active+"/get_logs?target="+target).read()
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
	return slave.objects.get(slave_hostname=hostname).slave_location
def ping_plot(request):
	target=request.GET.get('target')
	slaves_all=slave.objects.all()
	content={}
	for hosts in slaves_all:
		content[host_to_loc(hosts.slave_location)]=get_ping_logs(hosts.slave_hostname,target)
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
		json_obj['location']=str(log.slave_hostname)
		json_obj['timestamp']=str(log.timestamp)
		content[count]=json.dumps(json_obj)
		count = count + 1
	return HttpResponse(json.dumps(content))

def add_ping_log(target,hostname,respo):
	#check and filter if hostname and then convert it to location
	if respo!="":
        	try:
			slave_ob = slave.objects.get(slave_hostname=hostname)
			location =slave_ob.slave_location
			ping= ping_db(target=target,slave_hostname=location,result=respo)
		except:
			ping= ping_db(target=target,slave_hostname=hostname,result=respo)
        	ping.save()


def check_loading_time(request):
	target=request.GET.get('target')
	resp=[]
	json_obj={}
	all_slaves=slave.objects.all()
	for slave_active in all_slaves:
		reply=send_load_request(slave_active.slave_hostname,target)	
		resp.append(reply)
		json_obj[slave_active.slave_location]=reply
	#resp=send_load_request("mesos-slave1",target)
	return HttpResponse(json.dumps(json_obj))

def stress_test(request):
	target=request.GET.get('target')
	resp=[] 
	json_obj={}
	all_slaves=slave.objects.all()
	for slave_active in all_slaves:
		reply=send_stress_request(slave_active.slave_hostname,target)
		resp.append(reply)
		json_obj[slave_active.slave_location]=reply
	return HttpResponse(json.dumps(json_obj))
