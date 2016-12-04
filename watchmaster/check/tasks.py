from __future__ import absolute_import, unicode_literals
from celery import shared_task,task
import json, requests

@shared_task
def add(x, y):
    return x + y

from celery.task.schedules import crontab
from celery.task import periodic_task
from slaves.models import slave
from check.views import add_ping_log,send_ping_request
from check.models import monitor_db

def run_ping(target,hostname):
	resp=send_ping_request(hostname,target)
	add_ping_log(target,hostname,resp)
	check_down(target, resp)
	return 

def check_down(target, resp):
	resp_json = json.loads(resp)
	if int(resp_json) >= 50:
		send_alert(target)
	
def send_alert(target):
	payload = {}
	payload['username'] = "eig_hack"
	payload['token'] = "eig2016"
	payload['sender'] = "alert@restful.email"
	payload['to'] = ["azhar.h@endurance.com", "palash.o@endurance.com", "rahul.bu@endurance.com"]
	payload['subject'] = "ALERT!"
	payload['content'] = "DOWN!"
	#response = requests.post("https://api.restful.email/v1/send",data=json.dumps(payload))
	

@periodic_task(run_every=crontab())
def cron_ping():
	print "RUNNING CRON FOR PING"
	monitor_obs = monitor_db.objects.all()
	slaves_all = slave.objects.all()
	for obj in monitor_obs:
		for slav in slaves_all:
			run_ping(obj.target,slav.slave_hostname)
	
