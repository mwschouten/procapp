
from celery.result import AsyncResult, GroupResult
from celery.result import ResultBase
from celery.canvas import Signature  

def is_signature(a):
    return isinstance(a,Signature)

def is_async(a):
    return isinstance(a, ResultBase)

def get_status_async(a):
    """
    get the status and progress of an async result
    ResultBase covers both
    """
    if isinstance(a, GroupResult):

        if a.ready and a.successful() :
                status = 'SUCCESS'
                msg = {'total':len(a)}
        else:
            status =  'PROGRESS'
            msg = {'current':a.completed_count,'total':len(a)}
            
        if a.failed():
                errors = [r.result.message 
                            for r in a.results if r.failed()]
                msg.update({'error':{
                               'count_failed':len(errors),
                               'messages':set(errors) }})

    elif isinstance(a, AsyncResult):

        status = a.status
        msg = None

        if status == 'PROGRESS':
            msg = a.result
            if not msg.get('total'):  # in case of race condition
                msg = None

        if status=='FAILURE':
            msg = {'error':{
                               'count_failed':1,
                               'messages':[a.result.message] }}                

    else:
        return None

    print 'Checked status : ',status,msg

    return {'status':status,'msg':msg}




