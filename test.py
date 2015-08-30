import requests
from time import sleep

URL = 'http://127.0.0.1:8000/'

def goget(url):
    print 'URL : ', url
    r = s.get( URL + url )
    if r.ok:
        print r.json()
        return r.json()
    else:
        print 'Error :{}'.format(r.status_code)
        return r.status_code


s = requests.Session()

r1 = goget( 'check/Add/?a=6&b=7' )

hash = r1['result']['hash']

r2 = goget( 'run/' + hash )
while not r2[hash]==True:
    sleep(1)
    r2 = goget( 'run/' + hash )
