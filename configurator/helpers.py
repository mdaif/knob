from Exscript.protocols import Telnet
from Exscript import Account
from celery import chord
from celery.utils import uuid


class TelnetHandler(object):
    def __init__(self, host_address):
        self.host_address = host_address

    def __enter__(self):
        self.account = Account('mdaif', password='fat7yTE')
        self.conn = Telnet(debug=0, connect_timeout=None)
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