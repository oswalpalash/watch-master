# watch-master
The master server framework for monitoring. Click the screenshot to see it running on production.
[![ScreenShot](http://i.imgur.com/YTobPJA.png?1)](https://www.youtube.com/watch?v=uIJ7gNlhsYU)

##Install Instructions : 

1. Clone the watch-master repository on your master node.
2. Install the python modules described in requirements.txt
3. Install [rabbitmq-server](https://www.rabbitmq.com/download.html) on the master node.
4. Run the django server : 
```bash
cd watchmaster/
python manage.py runserver
```
5. Run the celery beat and celery worker:
```bash
celery worker --app=watchmaster -l info --logfile="/tmp/worker.log"
celery -A watchmaster beat
```


##To Add A [Slave](https://github.com/oswalpalash/watch-slave) Server : 
* Set up Slave as per : [Slave Repo](https://github.com/oswalpalash/watch-slave)
* Run the python shell prompt:
```bash
python manage.py shell
```
```python
from slaves.models import slave
slave_new = slave( slave_hostname=<hostname>, slave_ip=<ip>, slave_location=<location>)
slave_new.save()
```

* Make the corresponding changes in the [WATCH FRONTEND](https://github.com/oswalpalash/watch-frontend)
 part as well. 

