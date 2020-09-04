import uuid
from django.db import models
from django_cryptography.fields import encrypt
import datetime
from django.utils import timezone
from control.ipmi.rmcp import chassisStatus
from .utils import restore_int_to_str, last_event_str_converter
from ipmihub.env import downtime_delay



class Credential(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 200)
    username = models.CharField(max_length = 20)
    password = encrypt(models.CharField(max_length = 20))
    AccessLevels = [
        (2, 'User'),
        (3, 'Operator'),
        (4, 'Administrator')
    ]
    priv = models.IntegerField(choices = AccessLevels, default = 4)
    def __str__(self):
        return self.name
    


class Host(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 200)
    ip = models.CharField('IP', max_length = 45, blank = True)
    hostname = models.CharField(max_length = 253, blank = True)
    port = models.IntegerField(default = 623)
    connectChoices = [
        (True, 'IP'),
        (False, 'Hostname')
    ]
    ipC = models.BooleanField('Connect via IP Address', choices = connectChoices, default = True)
    cred = models.ForeignKey(Credential, on_delete = models.PROTECT)
    def __str__(self):
        return self.name
    def connection(self):
        return self.ip if self.ipC else self.hostname
    def powerStatus(self):
        return self.powerstatus_set.first()
    def powerValues(self):
        status = self.powerstatus_set.first()
        values = { i: status.__dict__[i] for i in status.fieldNames() }
        values['restore_policy'] = restore_int_to_str(values['restore_policy'])
        values['last_event'] = last_event_str_converter(values['last_event'])
        return values
    def online(self):
        return self.powerValues()['power_on']
    def errors(self):
        errors = []
        for key in self.powerStatus().errorFieldNames():
            if self.powerValues()[key]: errors.append(key) 
        if self.timeout(): errors.append('timeout')
        errors.sort()
        return errors
    def timeout(self):
        return self.powerStatus().time <= timezone.now() - datetime.timedelta(seconds=downtime_delay)
    
class PowerStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField(auto_now=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    power_on = models.BooleanField()
    overload = models.BooleanField()
    interlock = models.BooleanField()
    fault = models.BooleanField()
    control_fault = models.BooleanField()
    restore_policy = models.IntegerField()
    last_event = models.CharField(max_length=17)
    intrusion = models.BooleanField()
    front_panel_lockout = models.BooleanField()
    drive_fault = models.BooleanField()
    cooling_fault = models.BooleanField()
    def fieldNames(self):
        return set([field.name for field in self._meta.get_fields(include_parents=False)]) ^ {'id','time','host'}
    def errorFieldNames(self):
        return self.fieldNames() ^ {'power_on','restore_policy','last_event'}
    class Meta:
        ordering = ['-time']


