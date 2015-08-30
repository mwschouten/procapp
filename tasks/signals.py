# signals.py
django.db.models.get_model

from django.core.signals import post_save
from django.dispatch import receiver

@receiver(post_save)
def check_waiting(sender):
    print '+++++++++++++++++++++'
    print 'New result available :'
    print ' : ',sender
    print '+++++++++++++++++++++'