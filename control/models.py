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
        return PowerStatus.objects.filter(host = self, timeout=False).first()
    def powerValues(self):
        status = self.powerStatus()
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
        errors.sort()
        if self.timeout(): errors.append('timeout')
        return errors
    def timeout(self):
        status = self.powerstatus_set.first()
        return True if status.timeout else False
    
class PowerStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField(auto_now=True)
    timeout = models.BooleanField(default=False)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    power_on = models.BooleanField(null=True)
    overload = models.BooleanField(null=True)
    interlock = models.BooleanField(null=True)
    fault = models.BooleanField(null=True)
    control_fault = models.BooleanField(null=True)
    restore_policy = models.IntegerField(null=True)
    last_event = models.CharField(max_length=17, null=True)
    intrusion = models.BooleanField(null=True)
    front_panel_lockout = models.BooleanField(null=True)
    drive_fault = models.BooleanField(null=True)
    cooling_fault = models.BooleanField(null=True)
    def fieldNames(self):
        return set([field.name for field in self._meta.get_fields(include_parents=False)]) ^ {'id','time','host'}
    def errorFieldNames(self):
        return self.fieldNames() ^ {'power_on','restore_policy','last_event'}
    class Meta:
        ordering = ['-time']


