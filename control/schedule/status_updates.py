from control.models import Host, PowerStatus
from control.ipmi.rmcp import chassisStatus
import socket

def updateChassisStatus(host):
    try:
        state = chassisStatus(host.connection(),host.port,host.cred.username,host.cred.password)
        q = PowerStatus(host = host, **state)
        q.save()
    except socket.timeout:
        q = PowerStatus(host = host, timeout=True)
        q.save()
    

def updateAllHostStatus():
    for host in Host.objects.all():
        updateChassisStatus(host)
