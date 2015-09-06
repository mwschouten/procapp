from __future__ import absolute_import

from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from tasks.experts import tasks

from tasks.experts.tools.hbobject import HbObject
from tasks.experts.tools.celery_expert import get_status_async, is_async
from tasks.experts.tools.hbtask import check_stored_status

import tasks.models as models
import json
import time
import datetime

import sys,traceback
import inspect

## HELPERS
def available_hbtasks():
    """ iterate over all available hbtasks
    """
    out = []
    for tname in dir(tasks):
        t = getattr(tasks,tname)
        if inspect.isclass(t) and issubclass(t,tasks.HbTask) and t is not tasks.HbTask:
            yield tname, t

def tasks_that_make(thistype):
    return [name for name,task in available_hbtasks() if task().result.type==thistype]
    

## VIEWS
def options(request):
    """ return the available tasks with their api
    """
    out = {name:task().api for name, task in available_hbtasks()}
    return JsonResponse(out)



def results(request):
    """ return all saved results
    provide e.g. {'query':{'hb_taskname':'Add'}} to select specific.
    """
    print request
    print request.GET
    q = {k:v for k,v in request.GET.iteritems()}

    # q = request.GET.getlist('h')
    # if q is None:
    #     return JsonResponse({'Error':'provide query data with e.g. /?query={}'})

    # allow for selection based on result type
    thetype = q.pop('type',None)
    if thetype is not None:
        q['hb_taskname'] = q.get('hbtaskname',False) or tasks_that_make(thetype)

    rr = models.HBTask.objects.filter(status__gt=models.HBTask.NO_STATUS,**q)
    out = {'results':[r.description for r in rr]} if rr else {'results':None}
    return JsonResponse(out)


def check(request,task_name):
    """ check the settings of a HbTask
    return json with result hash, which you can then use to set up the next

    e.g. /check/Add/?x=1&y=5
    
    results in:
    {
        "taskname": "Add", 
        "settings": {
            "y": "5",
            "x": "1"
        },
        "result": {
            "hash": "5d8241df9311ef676a4aa5cea3b11a00",
            "type": "data"
        }
    }
    """
    try:
        todo = getattr(tasks,task_name,None)
    except KeyError:
        return JsonResponse(
            {'error':'This {} is not a known task'.format(taskname)})
    
    parameters = todo().settings.get.keys()
    
    try:
        kwargs = {par:request.GET[par] for par in parameters}
    except KeyError:
        return JsonResponse(
            {'error':'Missing parameter: please provide {}'.format(parameters)})

    action = todo(**kwargs)
    if not action.settings.valid:
        return JsonResponse(
            {'error':'Invalid settings: {}'.format(action.settings.errors)})

    action.set_result()
    return JsonResponse(action.description)


def available(request):
    """
    Check if hashes are already available
    
    E.g.
    
    /available/?h=1&h=2&h=1adf22a49521bb4da13686d2560953a6
    
    yields:

    {
        "1": false,
        "2": false,
        "1adf22a49521bb4da13686d2560953a6": true
    }

    E.g. for a result-group:

    /available/?h=d0f7b7149bc25933ef5e09ff5978a541
    """
    hashes = request.GET.getlist('h',None)
    available = {}
    for h in hashes:
        thisone = False
        try:
        # if True:
            stored = models.HBTask.objects.get(resulthash=h)

            print 'Look for ',h
            obj = HbObject(hash=h)

            # check if database status is still correct
            if stored.status < models.HBTask.OK_STATUS:
                check_stored_status(obj)

            # For an empty object, thow false
            print obj.content
            assert(obj.content)

            if is_async(obj.content):
                thisone = get_status_async(obj.content) or True
            else:
                thisone = True

        except Exception as e:
            print 'not available :',h
        
        available.update({h:thisone})

    return JsonResponse(available)


def status(request,resulthash):

    # Get from database
    try:
        stored_task = models.HBTask.objects.get(resulthash=resulthash)
    except Exception:
        return JsonResponse({'Error':'Could not load task'})
    pars = json.loads(stored_task.parameters)

    # Load the task with the parameters
    todo = getattr(tasks,stored_task.hb_taskname,None)
    T = todo(**pars)

    # Check the result    
    R = HbObject(T.result)

    t0 = datetime.datetime.fromtimestamp(R.log.date_first()).strftime('%Y-%m-%d %H:%M:%S')
    t1 = datetime.datetime.fromtimestamp(R.log.date_last()).strftime('%Y-%m-%d %H:%M:%S')
    out = { 'description'   : T.description,
            'log'           : {'text':R.log.data,'dates':[t0,t1]},
            'dependency_status'  : T.dependency_status()
        }

    return JsonResponse(out)



def run(request, resulthash):
    """ run what it takes to get me this hash
    """
    try:
        stored = models.HBTask.objects.get(resulthash=resulthash)
    except:
        stored = None
        thisone = {'Error', 'not found in database'}
    
    # Finished, and reported back
    if stored.status == models.HBTask.OK_STATUS:
        thisone = True

    # Submitted, have not heard from since
    elif stored.status == models.HBTask.PENDING_STATUS:
        obj = HbObject(hash=resulthash)
        status,fullstatus = check_stored_status(obj)
        thisone = fullstatus or True 

    # resulted in error
    elif stored.status == models.HBTask.ERROR_STATUS:
        thisone = {'Error','something'}

    # no status: submit now
    else:
        print 'Now status      : ',stored.status
        print 'Now submit task : ',stored.celery_taskname

        # to submit hb task
        todo = getattr(tasks,stored.hb_taskname)
        # celery_result = todo.delay(**json.loads(stored.parameters))
        parameters = json.loads(stored.parameters)
    
        action = todo(**parameters)

        if not action.ready_to_go:
            thisone = {'Warning':'Not all dependencies are met',
                        'dependency_status':action.dependency_status()}

            # Add me as waiting for a few
            todo = [d.split(':')[1] for d in action.dependencies_todo]
            dep = models.HBTask.objects.filter(resulthash__in=todo)
            for d in dep:
                w,isnew = models.Waiting.objects.get_or_create(todo=stored,dependency=d)
                print 'Created ? ',w,isnew
                # submit dependency to run
                run(None,resulthash=d.resulthash)
        else:
            action.submit()
            time.sleep(0.5)
            obj = HbObject(hash=resulthash)
            status,fullstatus = check_stored_status(obj)
            thisone = fullstatus or True 

    return JsonResponse({resulthash:thisone})
    # return JsonResponse(thisone)


def finished(request, resulthash):
    """ mark as finished, remove waiting for this one, start the waiting if it can
    """
    try:
        stored = models.HBTask.objects.get(resulthash=resulthash)
        stored.status = 2
        stored.save()
        thisone = 'Ok'
    except:
        thisone = {'Error':'not found in database'}
        
    # Check if anyone was waiting for thisone to finish:
    waiting_for_me = models.Waiting.objects.filter(dependency=stored)

    for w in waiting_for_me:       
        #  Submit the task waiting if there was only one dependency left
        if w.todo.waiting_set.count() == 1:
            run(None, resulthash=w.todo.resulthash)
        # remove this dependency
        w.delete()

    return JsonResponse({resulthash:thisone})


def info(request, resulthash):
    """ read info
    """
    h = HbObject(resulthash)
    return JsonResponse({resulthash:h.info})    

