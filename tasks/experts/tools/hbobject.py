from hblogger import HbLog
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

        if hash:
            self.load(hash=hash)
        else:
            self.type = getattr(self,'type', type)
            self.log = HbLog()
            self.log.head('HbObject type: {0:s}'.format(self.type))
            self.content = []

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
    def available(self, directory=os.path.abspath('.')):
        """ Check if my contenct are already available in a file
        """
        filepath = os.path.join(directory, 'hbhash', self.hash + '.p')
        return os.path.isfile(filepath)

    def save(self, directory=os.path.abspath('.')):
        dirpath = os.path.join(directory, 'hbhash')
        make_sure_path_exists(dirpath)
        filename = os.path.join(dirpath, self.hash + '.p')

        with open(filename, 'wb') as fid:
            pickle.dump(self.type, fid)
            pickle.dump(self.log.handler.data, fid)
            pickle.dump(self.content, fid, -1)

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
        if not self.available:
            raise Exception('File (hash=%s) not available' % hash)

        # Load type, log and contents from picked file
        filename = os.path.join(directory, 'hbhash', hash + '.p')
        with open(filename, 'rb') as fid:
            self.type = pickle.load(fid)
#            print 'just read TYPE :', self.type
            self.log = HbLog()
            self.log.handler.data = pickle.load(fid)
#            print 'just read LOG'
#            self.log.show()
            self.content = pickle.load(fid)
#            print 'just read CONTENT'
            # print self.content
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
