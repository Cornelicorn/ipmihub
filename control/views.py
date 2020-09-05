from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django_tables2 import SingleTableView
from django.urls import reverse
from .models import Host
from .tables import HostTable
from .ipmi import rmcp
from .schedule.status_updates import updateChassisStatus
import socket


class HostView(DetailView):
    model = Host
    template_name = 'control/host_detail.html'
    
class HostList(SingleTableView):
    model = Host
    table_class = HostTable
    template = 'control/host_list.html'

def powerControl(request, pk):
    host = Host.objects.get(pk=pk)
    command = int(request.POST['command'])
    try:
        rmcp.chassisCommand(host.connection(), host.port, host.cred.username, host.cred.password, command)
        updateChassisStatus(pk)
    except socket.timeout as e:
        raise e
    return HttpResponseRedirect(reverse('host', args=(host.id,)))