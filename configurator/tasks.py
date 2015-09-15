from __future__ import absolute_import
from celery import shared_task
from .helpers import TelnetHandler, flat_map
from django.core.mail import send_mail
from celery.contrib import rdb

@shared_task(name='tasks.configure_batch')
def configure_batch(ips, telnet_commands, username, password):
    results = []
    for ip in ips:
        try:
            with TelnetHandler(ip, username, password) as device:
                for telnet_command in telnet_commands:
                    device.execute(telnet_command.replace('\\r', '\r'))
        except Exception as e:
                results.append((False, ip, e.message))
        else:
            results.append((True, ip, None))

    return results

@shared_task(name='tasks.email_admin')
def email_admin(results_pairs, email):
    results_pairs = flat_map(results_pairs[0].get())
    failed = []
    succeeded = []
    for pairs in results_pairs:
        failed.extend(["{0}: {1}".format(pair[1], pair[2]) for pair in pairs if not pair[0]])
        succeeded.extend(["{0}".format(pair[1]) for pair in pairs if pair[0]])
    msg = ["The following destinations succeeded:\n", "\n".join(succeeded)]
    if failed:
        msg.append("\nThe following destinations failed:\n{0}".format( "\n".join(failed)))

    send_mail('Configurations Results', "".join(msg), 'support@knob.com', [email], fail_silently=False)
