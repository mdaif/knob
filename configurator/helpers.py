from Exscript.protocols import Telnet
from Exscript import Account
from celery import chord
from celery.utils import uuid
from django.conf import settings


class TelnetHandler(object):
    def __init__(self, host_address, username, password):
        self.host_address = host_address
        self.username = username
        self.password = password

    def __enter__(self):
        self.account = Account(self.username, password=self.password)
        self.conn = Telnet(debug=settings.TELNET_DEBUG_LEVEL, connect_timeout=None)
        self.conn.connect(self.host_address)
        self.conn.login(self.account)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.send('exit\r')
        self.conn.close(force=True)

    def execute(self, command):
        self.conn.execute(command)
        return self.conn.response


class ProgressChord(chord):
    """A proxy class that keeps track of the results"""
    def __call__(self, body=None, **kwargs):
        _chord = self.chord
        body = (body or self.kwargs['body']).clone()
        kwargs = dict(self,kwargs, body=body, **kwargs)
        if _chord.app.conf.CELERY_ALWAYS_EAGER:
            return self.apply((), kwargs)
        callback_id = body.options.setdefault('task_id', uuid())
        r = _chord(**kwargs)
        return _chord.AsyncResult(callback_id), r


def flat_map(nested):
    return [y for x in nested for y in x]