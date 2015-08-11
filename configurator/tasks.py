from __future__ import absolute_import
from celery import shared_task
from .helpers import TelnetHandler


@shared_task(name='tasks.configure_batch')
def configure_batch(ips, telnet_commands, username, password):
    for ip in ips:
        with TelnetHandler(ip) as device:
            for telnet_command in telnet_commands:
                device.execute(telnet_command)

    print "finished processing a batch !"
    return True

@shared_task(name='tasks.email_admin')
def email_admin(result, email):
    print "###############################"
    print "Finished .. emailing the admin"
    print result
    print email
    print "###############################"



@shared_task(name='tasks.test_chord')
def test_chord(results):
    print "#####"
    print results
    print "#####"

