from control.models import Host, PowerStatus
from control.ipmi.rmcp import chassisStatus
import socket

def updateChassisStatus(hostId):
    host = Host.objects.get(pk=hostId)
    try:
        state = chassisStatus(host.connection(),host.port,host.cred.username,host.cred.password)
    except socket.timeout as e:
        raise e
    q = PowerStatus(host = host, **state)
    q.save()

def updateAllHostStatus():
    for host in Host.objects.all():
        updateChassisStatus(host.id)
    