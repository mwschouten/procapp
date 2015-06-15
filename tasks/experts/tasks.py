# tasks expert
# from tasks.models import *

__author__ = 'mathijs'
from tools.hbobject import HbObject
from tools.hbtask import HbTask
from matlab_expert import call_matlab

from celery import group
from celery.result import AsyncResult
from celery import shared_task

import time

# # To test without django:
# from celery import Celery
# app = Celery('processing',backend='amqp')
# shared_task = app.task

@shared_task(name='SetupDensDist',bind=True,track_started=True)
# @app.task(name='SetupDensDist',bind=True,track_started=True)
def setup_pieces(mytask,parent,parameters):
    for i in range(10):
        mytask.update_state(state='PROGRESS',meta={'current':i,'total':10})
        time.sleep(1)
    return {'directory':'.',
            'depsi_rev':None,
            'function':'upper',
            'arguments':{'p':1},
            'buffers':[1,2,3]}

# @shared_task(name='SubmitDensDist',bind=True,track_started=True)
# @app.task(name='SubmitDensDist',bind=True,track_started=True)
def submit_pieces(mytask, setup, queue):
    return group( [call_matlab.s( 
                    directory=setup['directory'],
                    function=setup['function'],
                    arguments=setup['arguments'].update({buffer:buf}))
                for buf in setup['buffers']]
             )
  

# @shared_task(name='SubmitDensDist2',bind=True,track_started=True)
# @app.task(name='SubmitDensDist2',bind=True,track_started=True)
def submit_pieces_test(mytask, setup, queue):
    print 'SETUP : {}'.format(setup)     
    return group( [add.s(10,buf) for buf in setup['buffers']] )
    


@shared_task(name='add')
# @app.task(name='add')
def add(a,b):
    time.sleep(b)
    return a+b



class Add2(HbTask):

    def define(self):
        # Name, result
        self.longname = 'Add two numbers'
        self.name = 'Add'
        self.version = '0.1'
        self.result = HbObject('data')
        # Define settings
        self.settings.add('a',type=HbObject('data'))
        self.settings.add('b',type=HbObject('data'))
        self.runtask = add


class Add(HbTask):

    def define(self):
        # Name, result
        self.longname = 'Add two numbers'
        self.name = 'Add'
        self.version = '0.1'
        self.result = HbObject('data')
        # Define settings
        self.settings.add('a',type=float)
        self.settings.add('b',type=float)
        self.runtask = add


class DensifySetup(HbTask):

    def define(self):
        # Name, result
        self.longname = 'Setup densify distributed'
        self.name = 'SetupDensDist'
        self.version = '0.1'
        self.result = HbObject('setupdata')
        # Define settings
        self.settings.add('parent')
        self.settings.add('parameters')
        self.runtask = setup_pieces


class DensifyDistribute(HbTask):

    def define(self):
        # Name, result
        self.longname = 'Submit densify distributed'
        self.name = 'SubmitDensDist'
        self.version = '0.1'
        self.result = 'data'
        # Define settings
        self.settings.add('setup',HbObject('setupdata'))
        self.settings.add('queue',default='celery')
        self.runtask = submit_pieces_test





def test():
    """ Some basic testing (remove ./hbhash directory to really see it working)
    """
    import logging
    import time
    import celery.result


    # set up logging
    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(name)15s - %(levelname)s - %(message)s')
    logger = logging.getLogger('Test')
    formatter = logging.Formatter()

    # Do setup
    logger.info('Start test')
    d = DensifySetup(parent='aap',parameters={'a':1,'b':2})
    logger.info('Now run')
    d.run()
    logger.info('Done')
    logger.info('Result: {}'.format(str(d.result)))

    # # Reload result + show
    # logger.info('Now load result')
    # r = HbObject(d2.result)
    # if isinstance(r.content,AsyncResult):
    #     logger.info('Result: {}'.format(str(r.content.status)))
    # else:
    #     logger.info('Result: {}'.format(str(r.content)))

    # r = HbObject(d.result)



    d2 =  DensifyDistribute(setup=d.result,queue='celery')
    
    logger.info('Check ready to go')
    while not d2.ready_to_go:
        logger.info('  Not ready..')
        time.sleep(1)        

    logger.info('Now run distribution')
    d2.run()
    logger.info('Done')


    rr = HbObject(d2.result).content

    if isinstance(rr,celery.result.GroupResult):
        for i,r in enumerate(rr.results):
            if r.status=='SUCCESS':
                logger.info('Result ({}): {} {}'.format(i, r.status, str(r.result)))
            else:
                logger.info('Result ({}): {}'.format(i, r.status))

if __name__=='__main__':
    test()