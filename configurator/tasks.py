from __future__ import absolute_import
from celery import shared_task, task
import time


@shared_task(name='tasks.configure_batch')
def configure_batch(ips, commands):

    for ip in ips:
        print "configuring ip: {0}, applying commands: {1}".format(ip, commands)


