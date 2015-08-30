__author__ = 'mathijs'
import logging
from random import random
from hashlib import md5

class HbLogHandler(logging.StreamHandler):
    """
    To use with logging: handles in the sense that it
    keeps the messages in a variable. This allows for
    computation of the hash, and for storage with the
    rest of the object.
    """

    def __init__(self):
        super(HbLogHandler, self).__init__(stream=None)
        self.data = None

    def emit(self, record):
        try:
            self.data.append({
                'time': record.__dict__['created'],
                'level': record.__dict__['levelno'],
                'msg': record.__dict__['msg']
            })
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class HbLog():
    """
    Log for HB Objects
    Keep track of processing steps
    Provide unique hash based on processing history
    """
    def __init__(self, msg=None):
        self.handler = HbLogHandler()
        self.handler.data = []
        self.logger = logging.getLogger(str(random()))
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)
        self.logger.propagate = False
        if msg:
            self.head(msg)

    # Provide input levels
    def head(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    # def hash(self,data):
    #     """
    #     :return: md5 hash for the input
    #     """
    #     m = md5()
    #     m.update(data)
    #     return m.hexdigest()
    
    @property
    def hash(self):
        """
        Computes the hash from the object's log messages
        :return: md5 hash for the object
        """
        m = md5()
        [m.update(msg) for msg in self.data]
        return m.hexdigest()

    @property
    def data(self):
        return [l['msg'] for l in self.handler.data if l['level'] > logging.INFO]

    def date_first(self):
        return self.handler.data[0]['time']

    def date_last(self):
        return self.handler.data[-1]['time']

    # Show the log
    def show(self):
        frmt = {logging.DEBUG: '   {0[level]} : {0[msg]}',
                logging.INFO: '   {0[level]} : {0[msg]}',
                logging.WARNING: '*  {0[level]} : {0[msg]}  *',
                logging.ERROR: '** {0[level]} : {0[msg]} **',
                logging.CRITICAL: '** {0[level]} : {0[msg]} **'
        }
        for l in self.handler.data:
            print frmt[l['level']].format(l)



if __name__ == 'main':
    q = HbLog()
    q.head('aap')
    q.info({'aap': 'banaan', 'vis': 'sla'})
    q.head({'aap': 5, 'vis': 'haring'})
    print 'show log:'
    q.show()
    print '-----'
    print
    q2 = HbLog()
    q2.head('2 apen')
    print 'show log 2:'
    q2.show()
    print '-----'
