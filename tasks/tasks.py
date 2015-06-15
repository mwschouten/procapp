# tasks.py
# tasks.py
from __future__ import absolute_import
from celery import shared_task, chain
from celery.task.control import revoke

from proc.celery import app
#from catalogue.management.commands import update, datastats

import time

@shared_task(bind=True)
def test10sec(self):
    n=10

    for i in range(n):
        if not self.request.called_directly:
            self.update_state(state='PROGRESS',meta={'current': i, 'total': n})
        time.sleep(1)
    return

def randomerror():
    t = time.time()
    if int((t-int(t))*10)==5:
        raise Exception('Random error')

@shared_task
def give_error():
    raise Exception('This is an error message')
    return 1