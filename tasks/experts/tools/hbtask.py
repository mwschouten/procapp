from __future__ import absolute_import
__author__ = 'mathijs'

from .hbobject import HbObject
from .hbsettings import Settings
from .celery_expert import get_status_async, is_async

import json
import logging

# from celery import Task
from celery import Celery, chain
from celery.local import Proxy as CeleryTaskProxy
import celery.result 


def is_async(a):
    return isinstance(a, celery.result.ResultBase)


app = Celery('processing',backend='amqp')
# from celery.contrib.methods import task_method

# import traceback
# traceback.print_stack()

try:
    import tasks.models
    from tasks.experts.celery_expert import is_async, get_status_async
    DJANGO=True
    print 'DJANGO FOUND'
except:
    DJANGO=False
    print 'DJANGO NOT FOUND'



@app.task(name='SaveContent', ignore_result=True)
def save_hbobject_content(content,hash):
    print 'SAVE {} in {}'.format(content,hash)
    obj = HbObject(hash=hash)
    obj.log.info('Replace with finished content')
    obj.content = content
    obj.save()
    check_stored_status(obj)


# @app.task('LoadDepsAndRun', ignore_result=True)
# def load_deps_and_run(obj):

#     kwargs = self.settings.get
#     kwargs.update( self.load_dependencies() ) 

#     # Do the work and save it
#     result.content = chain( 
#             self.runtask.s(**kwargs), 
#             save_hbobject_content.s(resulthash)
#         ) ()




def check_stored_status_hash(hash):
    try:
        obj = HbObject(hash=hash)
    except:
        raise Exception('Not found {}'.format(hash))
    check_stored_status(obj)


def check_stored_status(obj):
    if DJANGO:
        print 'CHECK STATUS OF ',obj.hash
        stored = tasks.models.HBTask.objects.get(resulthash=obj.hash)
        if not stored:
            raise Exception('Not Stored {}'.format(obj.hash))

        if is_async ( obj.content ):
            status_checked = get_status_async(obj.content).get('status')
            newstatus = {
                             'FAILURE':  tasks.models.HBTask.FAIL_STATUS,
                             'SUCCESS':  tasks.models.HBTask.OK_STATUS,
                             'PROGRESS': tasks.models.HBTask.PENDING_STATUS,
                             'PENDING':  tasks.models.HBTask.PENDING_STATUS
                            }.get(status_checked)
        else:
            newstatus = tasks.models.HBTask.OK_STATUS

        if not newstatus == stored.status:
            print 'Change status of {} from {} to {}'.format(obj.hash,stored.status,newstatus)
            stored.status = newstatus
            stored.save()


# @app.task(name='HbRunTask')
# def run_task(task,hash,**kwargs):
#     print 'RUN {} for {}'.format(task, hash)
#     a =  chain( 
#             task.s(**kwargs), 
#             save_hbobject_content.s(hash))()
#     print 'TASKID A ',a.task_id
#     print 'PARENT A ',a.parent



class HbTask():
    """
    A task that takes zero or more HbObjects, 
    does something, and returns another HbObject.
    """


    def __init__(self,log=None,**kwargs):

        self.name = ''
        self.version = ''
        self.settings = Settings()
        self.result = None

        # overload this define 
        self.define()

        # user short name if there is no long one
        self.longname = getattr(self,'longname',self.name)

        # celery task
        self.name = getattr(self,'name',self.longname.title().replace(' ',''))
        self.log = logging.getLogger(self.name)


        # Set settings
        self.settings.set(**kwargs)


        if isinstance(self.runtask,celery.local.Proxy):
            self._do_runtask = self.runtask.s
        elif callable(self.runtask):
            self._do_runtask = self.runtask
        else:
            self.log.error('The runtask should be a shared_task or something running quickly that returns an AsyncResult')

    def define(self):
        """ TO BE OVERLOADED
        """
        pass

    def execute(self,**kwargs):
        """ TO BE OVERLOADED
        """
        return none

    def set_result(self):
        """ Based on the settings, compute the result hash and save an empty result file.
        """

        if self.settings.valid:

            # Create result log/hash
            if isinstance(self.result,HbObject):
                result = self.result
            else:
                result = HbObject(self.result)

            result.log.head(self.longname+' v. '+self.version)
            for k,v in self.settings.getstr.iteritems():
                result.log.head('  {} : {}'.format(k,v))
            
            # If new, save empty
            if not result.available:
                result.save()
            
            # Use shorthand version
            self.result = result.typehash

            self.log.info('SAVE TO DJANGO {}'.format(DJANGO))
        
        else:
            self.log.error('Try to set without proper settings')


    @property
    def ready_to_go(self):
        """ Tell me if the task is ready to go: all dependencies are met
        """
        deps = self.load_dependencies()
        return not any([ is_async(d) for d in deps.values()])
            
    def wait_for_these(self):
        return [ d for d in deps.values() if is_async(d)]
        

    def load_dependencies(self):
        """ load all dependencies to be given to 'execute'
        """
        deps = {}
        for i in self.dependencies:
            deps[i] = HbObject(hash=self.settings.get[i]['hash'],
                               type=self.settings.get[i]['type']).content
        return deps


    def run(self):
        """ Really do something here: wrap the specific 'execute'
        """

        self.set_result()
    
        if not self.result:
            self.log.error('Settings not valid')
            return

        # try if we already have this item
        # The task has already been submitted and saved 
        resulthash = self.result['hash']
        result = HbObject(hash=resulthash)
        if result.content:
            self.log.info('Result already found ({})'.format(resulthash))
            self.log.info('Result: {}'.format(result.content))
            # show progress 
            self.log.info('Progress : {}'.format(get_status_async(result.content)))

        # Otherwise, submit it now
        else:
            if DJANGO:
                self.save_task()

            self.log.info('Start {} for {}'.format(self.name, resulthash))
            # All the arguments to the task: dependencies loaded, and settings            



            kwargs = self.settings.get
            kwargs.update( self.load_dependencies() ) 

            # Do the work and save it
            result.content = chain( 
                    self._do_runtask(**kwargs), 
                    save_hbobject_content.s(resulthash)
                ).delay()

            if DJANGO:
                self.save_run(result.content.task_id)

            self.log.info('Submitted {}'.format(resulthash))
            # for the time being, we store the complete chain as the result
            result.save()

        
    if DJANGO:
        def save_run(self,task_id):
            try:
                stored_task = tasks.models.HBTask.objects.get(resulthash=self.result['hash'])
            except:
                raise Exception('Not found stored task with hash='.format(self.result['hash']))


            stored_run = tasks.models.HBTaskRun.objects.create(
                task = stored_task,
                celery_id = task_id,
            )

        def save_task(self):
            self.log.info('SAVE TASK TO DATABASE')
            stored_task, isnew = tasks.models.HBTask.objects.get_or_create(
                celery_taskname = self.runtask.name,
                parameters = json.dumps(self.settings.get),
                resulthash = self.result['hash'],
            )
            if isnew:
                stored_task.status = tasks.models.HBTask.PENDING_STATUS
                stored_task.save()
            self.log.info('SAVED WITH ID {}'.format(stored_task.id))

    @property
    def done(self):
        self.set_result()
        return self.result.available

    @property
    def todos(self):
        return [self.settings.get[d] for d in self.dependencies
                if not self.settings.get[d].available]

    @property
    def dependencies(self):
        return self.settings.dependencies

    @property
    def json(self):
        return json.dumps(
            {'name':self.name,
             'version':self.version,
             'settings':self.settings.getstr,
             'dependencies':self.settings.dependency_dict,
             'result': self.result})


# #    @celery.task
#     def execute(self):
#         """
#         Perform the action through celery queue handlers
#         Workers are activated using:    celery -A tasks worker --loglevel=info

#         During the execution, we produce the content carried in
#         self.result.content

#         """
#         print '----------------------------------------'
#         print 'Now executing the HbTask'
#         print '----------------------------------------'
#         print 'name     -> ', self.name
#         print 'settings -> ', self.settings.get
#         print 'result   -> ', self.result
#         print '----------------------------------------'
#         self.result.content = [1,2,3]
#         self.result.save()


# if True:
#    p0 = Polygon()
#    p0.log.head('Niks mee gedaan')
#    print 'log of p0:'
#    p0.log.show()
#    print '--> ',p0.hash
#    print
#
#    p1 = BufferPolygon(parent=p0, bufferwidth=100)
#
#
#    print 'log of p1:'
#    p1.result.log.show()
#    print '--> ',p1.result.hash
#
