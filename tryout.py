
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proc.settings")
django.setup()

import shutil
import requests
from pprint import pprint
from tasks import models
from time import sleep

BASE_URL = 'http://127.0.0.1:8000/'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_progress(h):
    print bcolors.HEADER + h + bcolors.ENDC

def print_ok(h):
    print bcolors.OKBLUE + h + bcolors.ENDC

def print_response(h):
    print bcolors.OKGREEN 
    pprint(h)
    print bcolors.ENDC

def print_error(h):
    print bcolors.FAIL + h + bcolors.ENDC


def req(url,*pars):
    try:
        if pars:
            url = url.format(*pars)
        print 'REQUEST : ',url
        r = requests.get(url)
        if r.ok:
            return r.json()
        else:
            print_error('ERROR : no response')
            print_response('Status {}'.format(r.status))
            return None
    except Exception as e:
        print_error('Error : '+url)
        print_error(str(e))

def check_status(hh,wait=False):
    print 'Check status:'
    ok = False
    while not ok:
        url = BASE_URL + 'api/available/'
        url = url + '?h=' + '&h='.join(hh)

        # print_ok ('URL : '+url)
        s= req(url)
        print s
        for h in hh:
            print_progress('  {} : {}'.format(h,s[h]))
        print 
        ok = all([i==True for i in s.values()])
        # print s.values()
        if not wait:
            return
        sleep(2)


def cleanup():

    print_progress('Clean up')
    # remove from database
    for t in models.HBTask.objects.all():
         t.delete()
    for t in models.Waiting.objects.all():
         t.delete()

    # remove physically
    if os.path.exists('hbhash'):
        shutil.rmtree('hbhash')


def setup():

    url = BASE_URL + 'api/check/Add/?a={}&b={}'
    r1 = req(url,1,2)
    r2 = req(url,2,3)

    print 'r1 : ',r1

    h1 = r1['result']['hash']
    h2 = r2['result']['hash']

    print 'add 1+2 :', h1
    print 'add 2+3 :', h2

    # Thirs step: add the two results
    r3 = req(BASE_URL + 'api/check/Add2/?a={}&b={}',h1,h2)
    h3 = r3['result']['hash']
    print '\nadd two results :', h3

    check_status([h1,h2,h3])
    return h1,h2,h3


def main():
    cleanup()
    h1,h2,h3 = setup()
    #  Not yet available (nothing is)
    print_progress('\nAvailablility of third step?')
    print_response(req(BASE_URL + 'api/available/?h={}',h3))
    check_status([h1,h2,h3])


    # Now run one
    r1 = req(BASE_URL + 'api/run/{}',h1)
    check_status([h1],wait=True)

    print_progress('\ndependency status of third:')
    print_response(req(BASE_URL + 'api/status/{}',h3)['dependency_status'])

# print '\nNow wait two seconds'
# for i in range(5):
#     sleep(0.5)
#     check_status(h1,h2,h3)


    print_progress('\nTry to run third step:')
    r5 = req(BASE_URL + 'api/run/{}',h3)
    print_response(r5)

    print_progress ('\nNow wait for all results')
    ok = check_status([h1,h2,h3],wait=True)

# print '\nTry to run third step: (again)'
# r5 = req(url,h3)
# pprint(r5)

if __name__=="__main__":
    main()

