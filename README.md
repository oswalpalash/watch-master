# watch-master
The master server framework for monitoring. Click the screenshot to see it running on production.
[![ScreenShot](http://i.imgur.com/YTobPJA.png?1)](https://www.youtube.com/watch?v=uIJ7gNlhsYU)

##Install Instructions : 

Clone the watch-master repository on your master node.
Install the python modules described in requirements.txt
Install [rabbitmq-server](https://www.rabbitmq.com/download.html) on the master node.
Run the django server : 
->cd watchmaster/
->python manage.py runserver
Run the celery beat and celery worker:
->celery worker --app=watchmaster -l info --logfile="/tmp/worker.log" 
->celery -A watchmaster beat


##To Add A Slave Server : 

Run the python shell prompt:
->python manage.py shell
$> from slaves.models import slave
$> slave_new = slave(slave_hostname=<hostname>, slave_ip=<ip>, slave_location=<location>)
$> slave_new.save()
Make the corresponding changes in the front-end part as well. 

