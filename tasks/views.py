from __future__ import absolute_import

from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from tasks.experts import tasks

from tasks.experts.tools.hbobject import HbObject
from tasks.experts.tools.celery_expert import get_status_async, is_async
from tasks.experts.tools.hbtask import check_stored_status

import tasks.models as models

def check(request,task_name):
    """ check the settings of a HbTask
    return json wi result hash, which you can then use to set up the next

    e.g. /check/Add/?x=1&y=5
    
    results in:
    {
        "taskname": "Add", 
        "settings": {
            "y": "5",
            "x": "1"
        },
        "ok": true,
        "result": {
            "hash": "5d8241df9311ef676a4aa5cea3b11a00",
            "type": "data"
        }
    }
    """
    try:
        todo = getattr(tasks,task_name,None)
        print 'TASKS NOW :',tasks
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
            {'error':'Invalid settings: {}'.format(action.settings.get)})

    action.set_result()
    # action.run()
    # print action.result
    return JsonResponse({'ok':True,
                         'taskname':task_name,
                         'settings':action.settings.get,
                         'result':action.result})


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
        try:
        # if True:
            stored = models.HBTask.objects.get(resulthash=h)

            obj = HbObject(hash=h)

            if stored.status == models.HBTask.PENDING_STATUS:
                check_stored_status(obj)

            thisone = get_status_async(obj.content) or True

        except:
            thisone = False
        available.update({h:thisone})
    # available = {h:HbObject(h).available for h in results}
    return JsonResponse(available)

