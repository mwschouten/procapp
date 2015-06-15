
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

class Setting:

    def __init__(self, name, 
                 default=None,
                 mandatory=True,
                 validate=None,
                 type=lambda x:x):

        assert isinstance(name, str)
        self.name = name
        self.type=type

        if isinstance((default),HbObject):
            self.value = self.default = default.typehash
            self.dependency = True
        else:
            self.value = self.default = default
            self.dependency = False

        self.mandatory = mandatory

        if validate:
            self.validate = validate

    def __unicode__(self):
        return 'Setting {} [{}]'.format(self.name, self.default)


    def validate(self, testval):
        """ Validate a single setting w.r.t. type etc. """
        if self.type:
            try:
                self.type(testval)
            except:
                return False
        return True

    def set(self, val):
        if isinstance(val, HbObject):
            val = val.typehash
        totype = getattr(self,'type', lambda x:x)
        self.value = totype(self.validated(val))

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
        for k, v in kwargs.iteritems():
            if k in self.settings.keys():
                self.settings[k].set(v)
            else:
                logging.error('{} is not a setting'.format(k))

    @property
    def get(self):
        """
        Show currently set settings (also inferred from default)
        -> normal key:value dict with whatever it is
        """
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
        #return {i:{'type':self.get[i].type,'hash':self.get[i].hash}
        #           for i in self.dependencies}

    @property
    def mandatory(self):
        return {name:s for name,s in self.settings.iteritems() if s.mandatory}

    @property
    def valid(self):
        ok = [v.value for v in self.settings.values() if v.mandatory]
        return all(ok)

class NotValidError(Exception):
    def __init__(self, value, parameter):
        self.msg = 'ERROR: "{}" is not a valid setting for "{}"'.format(value, parameter)


if __name__=='__main__':

    s = Setting('aap')
    s.set('Banaan')

    S = Settings()
    S.add('aap')
    S.add('banaan',validate = lambda x: (x>3))
    S.set(aap=1,banaan=5)