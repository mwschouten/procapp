
__author__ = 'mathijs'
import collections
from hbobject import HbObject
import logging
# e.g.
# dependencies =
#   {
#   'parent':{'default': PointSet()}
#
# settings =
#   {
#   'model':{
#       'default':['linear','seasonal'],
#       'help'   :'Model to use in least squares parameter estimation',
#       'valid_set'  :['linear','seasonal','quadratic','cubic','custom'],
#   'custom':{
#       'default':[],
#       'help'   :'Custom timeseries to use as model component',
#   'slcweight':{
#       'default':[],
#       'help'   :'Weights to apply to each timestep in parameter estimation',
#       'item_type'   :float,
#       'valid_range'  :[0,1]}
#   }

def ishash(s):
    return len(s)==32 and all([chr(i) for i in range(48,58)+range(97,103)])

class Setting:

    def __init__(self, name, 
                 default=None,
                 mandatory=True,
                 validate=None,
                 type=None):

        assert isinstance(name, str)
        self.name = name
        self.type = type

        if type is None:
            if default is None:
                self.type = lambda x:x
            else:
                self.type = __builtins__['type'](default)

        if isinstance((type),HbObject):
            default = None
            self.dependency = True
        else:
            self.dependency = False
            
        self.value = self.default = default
        self.mandatory = mandatory

        if validate:
            self.validate = validate

    def __unicode__(self):
        return 'Setting {} [{}]'.format(self.name, self.default)

    @property
    def description(self):
        """ description of the setting
        """
        if isinstance(self.type,HbObject):
            tp = self.type.type
        else:
            tp = self.type
        return {'name':self.name,'type':str(tp),'mandatory':self.mandatory,'default':str(self.default)}

    def validate(self, testval):
        """ Validate a single setting w.r.t. type etc. """
        # check hbobject type
        if self.type and isinstance(self.type,HbObject):
            try:
                assert( type(testval) in [str,unicode] and testval.find(':')>0)
                tt,hh = testval.split(':')
                assert(len(hh)==32)
                assert(self.type.type == tt)
            except Exception, e:
                logging.error(e, exc_info=True)
                logging.error('expected HbObject {}, got {}'.format(self.type.type,testval))
                return False
        # or try to cast to requested type
        else:    
            try:
                self.type(testval)
            except Exception, e:
                logging.error('cannot cast this {} to {}'.format(testval, self.type))
                logging.error(e, exc_info=True)
                return False
        return True

    def set(self, val):
        if isinstance(val, HbObject):
            val = str(val)
        elif ishash(val):
            # TODO: gettype: read only the type from hbobject instead of all data?
            # TODO: alternatively, get type from database.
            try:
                val = str(HbObject(hash=val))
            except Exception as e:
                raise NotValidError(val,self.name,e.message)

        self.value = self.validated(val)

    def validated(self,testval):
        # if True:
        # groups are resubmitted ech separately
        if isinstance(testval, list): #or isinstance(testval, dict):
                ok = all([self.validate(i) for i in testval])
        else:
                ok = self.validate(testval)
        if ok:
            return testval
        else:
            raise NotValidError(testval,self.name)

class Settings:
    def __init__(self):
        self.settings = {}

    def add(self, *args, **kwargs):
        """ Add a parameter to the settings

        Parameters:

        positional:
            name
            default

        key=value:
            :key        :default
            mandatory   False
            help        ''
            dependency  False
        """
        new = Setting(*args, **kwargs)
        self.settings.update({new.name: new})

    def set(self, **kwargs):
        """ Set one or more parameters
        e.g. set({'aap':'piet', 'banaan':'geel'}
        """
        self.errors = []
        for k, v in kwargs.iteritems():
            if k in self.settings.keys():
                try:
                    self.settings[k].set(v)
                except Exception as e:
                    self.errors.append(e.msg)
            else:
                logging.error('{} is not a setting'.format(k))

    @property
    def get(self):
        """
        Show currently set settings (also inferred from default)
        -> normal key:value dict with whatever it is
        """
        # for k,v in self.settings.iteritems():
        #     print k,v,type(v)
        return {k: v.value for k, v in self.settings.iteritems()}

    @property
    def getstr(self):
        """
        Give currently set settings (also inferred from default)
        -> value always as a string
        """
        return {k: str(v.value) for k, v in self.settings.iteritems()}

    @property
    def dependencies(self):
        return [s.name for s in self.settings.values() if s.dependency]

    @property
    def dependency_dict(self):
        return {i:self.get[i] for i in self.dependencies}

    @property
    def mandatory(self):
        return {name:s for name,s in self.settings.iteritems() if s.mandatory}

    @property
    def description(self):
        """ description of the settings
        """
        out = {}
        for name,sett in self.settings.iteritems():
            d = {k:v for k,v in sett.description.iteritems() if k is not 'name'}
            out[name] = d
        return out

        if isinstance(self.type,HbObject):
            tp = self.type.type
        else:
            tp = self.type
        return {'name':self.name,'type':str(tp),'mandatory':self.mandatory,'default':self.default}

    @property
    def valid(self):
        ok = [v.value for v in self.settings.values() if v.mandatory]
        return all(ok)

class NotValidError(Exception):
    def __init__(self, value, parameter,reason=None):
        self.msg = '{} is not a valid setting for {} ({})'.format(value, parameter, reason)


if __name__=='__main__':

    s = Setting('aap')
    s.set('Banaan')

    S = Settings()
    S.add('aap')
    S.add('banaan',validate = lambda x: (x>3))
    S.set(aap=1,banaan=5)