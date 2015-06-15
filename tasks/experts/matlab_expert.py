
# cmm = """~/helpers/matlab_batch "DePSI_rev='mathijs'; run ~/software/DePSI/pathsetup.m; densify_one_buffer('{}')" """
# .format(s)
from celery import Celery
app = Celery('processing',backend='amqp')

@app.task
def call_matlab(    directory='.',
                    depsi_rev=None,
                    function=None,
                    arguments=None,
                    batch_call='~/helpers/matlab_batch'):
    
    with cd( directory ):    
        
        # format the arguments as a single json blob
        s=json.dumps(arguments)
        s=s.replace('"',r'\"')

        for_depsi = ''
        if depsi_rev:
            for_depsi = "DePSI_rev='{}'".format(depsi_rev)

        # setup the matlab batch call    
        cmm = ("""{} "{}; """
               """run ~/software/DePSI/pathsetup.m;""" 
               """ {}('{}')" """).format(batch_call, for_depsi, function, s)
    
        # run it
        return subprocess.call(cmm,shell=True)
  