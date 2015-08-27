
from __future__ import absolute_import

from tasks.experts import tasks as currently_available_tasks
import tasks.models

def load_task_from_db(hash):

    stored_task = tasks.models.HBTask.objects.get(resulthash=hash)
    self.log.info('LOAD FROM DATABASE')
    # stored_task.hb_taskname = self.name
    # stored_task.celery_taskname = self.runtask.name
    # stored_task.parameters = json.dumps(self.settings.get)
    # stored_task.status = tasks.models.HBTask.NO_STATUS

    T = getattr(currently_available_tasks,stored_task.celery_taskname,None)
    pars = json.loads(stored_task.parameters)
    T.settings.set(**q)
    return T




