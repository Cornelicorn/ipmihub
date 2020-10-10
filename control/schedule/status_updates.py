from control.models import Host, PowerStatus, SensorStatus, SensorReading, SensorSetting
from control.ipmi.rmcp import chassisStatus, sensorStatus
import socket

def updateChassisStatus(host):
    try:
        state = chassisStatus(host.connection(),host.port,host.cred.username,host.cred.password)
        q = PowerStatus(host = host, **state)
        q.save()
    except socket.timeout:
        q = PowerStatus(host = host, timeout=True)
        q.save()
    
def updateSensorStatus(host):
    try:
        state = sensorStatus(host.connection(),host.port,host.cred.username,host.cred.password)
        sensor_status = SensorStatus(host = host)
        sensor_status.save()
        for dict in state:
            thresholds = dict['thresholds']
            del dict['thresholds']
            for key in ['unr', 'ucr', 'unc', 'lnc', 'lcr', 'lnr']:
                globals()['thresholds_' + key] = thresholds[key] if thresholds else None

            settings = SensorSetting.objects.filter(host = host, sensor_id = dict['sensor_id']).first()
            if not settings:
                settings = SensorSetting(host = host, sensor_id = dict['sensor_id'],
                                        thresholds_unr = thresholds_unr,
                                        thresholds_ucr = thresholds_ucr,
                                        thresholds_unc = thresholds_unc,
                                        thresholds_lnc = thresholds_lnc,
                                        thresholds_lcr = thresholds_lcr,
                                        thresholds_lnr = thresholds_lnr)
                settings.save()
            
            q = SensorReading(sensor_status = sensor_status, **dict)
            q.save()
    except socket.timeout:
        q = SensorStatus(host = host, timeout=True)
        q.save()

def updateAllHostStatus():
    for host in Host.objects.all():
        updateChassisStatus(host)
        updateSensorStatus(host)