import datetime

from django.db import models
# from django.contrib.gis.db import models
# Create your models here.
# class PointLP(models.Model):
# class PointSet(models.Model):


class HBTask(models.Model):
    
    PENDING_STATUS=0
    OK_STATUS=1
    FAIL_STATUS=2
    STATUS_CHOICES=((PENDING_STATUS,'Pending'),(OK_STATUS,'Done'),(FAIL_STATUS,'Failed'))

    celery_taskname = models.CharField(max_length=100,blank=False)
    parameters      = models.TextField(null=True,blank=True)
    resulthash      = models.CharField(max_length=32,blank=True,null=True)
    status          = models.IntegerField(choices=STATUS_CHOICES,default=PENDING_STATUS)
    submitted       = models.DateTimeField(default = datetime.datetime.now())


    def __str__(self):
        return '{} for {} ({})'.format(self.celery_taskname,self.resulthash, 
            self.STATUS_CHOICES[self.status][1])

class HBTaskRun(models.Model):
    """
    Attempts to run a HBTask
    """
    task        = models.ForeignKey(HBTask)
    celery_id   = models.CharField(max_length=50,blank=True,null=True,unique=True)
    picked_up   = models.DateTimeField(default = datetime.datetime.now())
    error       = models.TextField(null=False,blank=True)
    done        = models.BooleanField(default=False)

    def __str__(self):
        if self.done:
            return 'DONE {} / {}'.format(self.task,self.celery_id)
        elif self.error:
            return 'ERROR {} / {}'.format(self.task,self.celery_id)
        else:
            return 'PENDING {} / {}'.format(self.task,self.celery_id)



