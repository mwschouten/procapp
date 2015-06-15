class Setting:
    def __init__(self, name, 
                 default=None,
                 mandatory=True):

        self.name = name
        self.mandatory = mandatory

    def validated(self,a):
        return a

    def set(self, val):

        self.value = self.validated(val)
        print 'Value of {} is now {}'.format(self.name,val)

s = Setting('aap')
s.set('Banaan')