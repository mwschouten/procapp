from hblogger import HbLog
from celery_expert import is_async
import os
import errno
import json
import pickle

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return


class HbObject():
    """ General purpose object. Provides a log and hash for bookkeeping
    Can save and load its content, if any.
    """
    def __init__(self, type='', hash=None):
        """ Start
        """
        # in case you initiate with the typehash dict 
        if isinstance(type,dict):
            hash=type.get('hash',None)
            type=type.get('type','')
        # elif isinstance(type,str) and type.find(':'):
        #     try:
        #         tt,hh = type.split(':')
        #         assert(len(hash)==32)
        #         type,hash=tt,hh
        #     except:
        #         pass

        if hash:
            self.load(hash=hash)
        else:
            self.type = getattr(self,'type', type)
            self.log = HbLog()
            self.log.head('HbObject type: {0:s}'.format(self.type))
            self.content = []


    def __call__(self,*args,**kwargs):
        """ Make an object of my own type, with new settings:
        To derive from an 'empty' object which has just type,
        makes sure that the new thing has the same type.
        """
        q = HbObject(*args,**kwargs)
        assert(q.type == self.type)
        return q

    @property
    def hash(self):
        """ Computes the hash from the object's log messages
        """
        return self.log.hash

    @property
    def json(self):
        return json.dumps(self.typehash)

    @property
    def typehash(self):
        return {'type':self.type,'hash':self.hash}

    def __unicode__(self):
        return self.type + ':' + self.hash

    def __str__(self):
        return self.type + ':' + self.hash      

    @property
    def known(self, directory=os.path.abspath('.')):
        """ Check if this thing is already in a file
        """
        filepath = os.path.join(directory, 'hbhash', self.hash + '.p')
        return os.path.isfile(filepath)

    @property
    def available(self, directory=os.path.abspath('.')):
        """ Check if my content are already available in a file
        """
        return self.status==2

    @property
    def status(self):
        """ give 0,1,2 for no, temporary or real content
        TODO what if we mean to save 'false' as proper content?
        """
        if not self.known:
            return 0 # no file yet
        self.load()

        if not self.content:
            return 0
        else:
            if is_async(self.content):
                return 1 # temporary content
            else:
                return 2 # real content
        

    def save(self, directory=os.path.abspath('.'),status=0):
        """ save contents to pickled file
        TODO replace by freeform database?
        """
        dirpath = os.path.join(directory, 'hbhash')
        make_sure_path_exists(dirpath)
        filename = os.path.join(dirpath, self.hash + '.p')

        with open(filename, 'wb') as fid:
            pickle.dump(self.type, fid)
            pickle.dump(self.log.handler.data, fid)
            pickle.dump(self.content, fid, -1)

        print 'HBOBJECT NOW SAVED {}'.format(self.hash)
        self.log.show()
        print 'HBOBJECT CONTENT   {}'.format(self.content)
        return


    def load(self, directory=os.path.abspath('.'), hash=None):
        """ Load the object from a pickled file
        you can give the directory to look in, otherwise use './hbhash/'
        you may provide the hash of the object you want, otherwise use my own
        (from current log)
        """
        # use my own hash if none provided
        # if isinstance(hash,dict):
        #     hash= hash.get('hash',None)
        self.hash = hash or self.hash

        # Just continue when I am available
        if not self.known:
            raise Exception('File (hash=%s) not available' % self.hash)

        # Load type, log and contents from picked file
        filename = os.path.join(directory, 'hbhash', self.hash + '.p')
        with open(filename, 'rb') as fid:
            self.type = pickle.load(fid)
            self.log = HbLog()
            self.log.handler.data = pickle.load(fid)
            self.content = pickle.load(fid)
        return True


if __name__ == '__main__':
#if True:

    def make(self):
        self.log.head('Hier is iets gebeurd')
        self.content = 'Uitkomst'

    a = HbObject('test')

    a.log.show()
    print 'Hash is now: ', a.hash
    print

    print 'Doe iets kleins'
    a.log.info('Doe iets')
    a.log.show()
    print 'Hash is now: ', a.hash
    print

    a.save()
    first_hash = a.hash

    print 'Doe iets groots'
    make(a)
    a.log.show()
    print 'Hash is now: ', a.hash
    print a.content
    print
