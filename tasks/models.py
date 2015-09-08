import datetime
import json

from django.db import models
# from django.contrib.gis.db import models
# Create your models here.
# class PointLP(models.Model):
# class PointSet(models.Model):


class HBTask(models.Model):
    NO_STATUS = 0
    PENDING_STATUS=1
    OK_STATUS=2
    ERROR_STATUS=-1
    STATUS_CHOICES=(
        (NO_STATUS,'Not submitted'),
        (PENDING_STATUS,'Pending'),
        (OK_STATUS,'Success'),
        (ERROR_STATUS,'Failure'))

    hb_taskname = models.CharField(max_length=100,blank=False)
    celery_taskname = models.CharField(max_length=100,blank=False)
    parameters      = models.TextField(null=True,blank=True)
    resulthash      = models.CharField(max_length=32,blank=True,null=True)
    resulttype      = models.CharField(max_length=100,blank=False)
    status          = models.IntegerField(choices=STATUS_CHOICES,default=NO_STATUS)
    submitted       = models.DateTimeField(default = datetime.datetime.now())

    def __str__(self):
        return '{} for {} ({})'.format(self.hb_taskname,self.resulthash[0:10], 
            self.STATUS_CHOICES[self.status][1])

    @property
    def description(self):
        """ Describe
        """
        return {'taskname':self.hb_taskname,
                'settings':json.loads(self.parameters),
                'result':{'hash':self.resulthash,'type':self.resulttype},
                'status':self.STATUS_CHOICES[self.status][1]
                }



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
            return 'SUCCESS {} / {}'.format(self.task,self.celery_id)
        elif self.error:
            return 'ERROR {} / {}'.format(self.task,self.celery_id)
        else:
            return 'PENDING {} / {}'.format(self.task,self.celery_id)


class Waiting(models.Model):
    todo = models.ForeignKey(HBTask)
    dependency = models.ForeignKey(HBTask,related_name='dependency')

    def __str__(self):
        return '{} waiting for {}'.format(
            self.todo.resulthash[0:10],self.dependency.resulthash[0:10])