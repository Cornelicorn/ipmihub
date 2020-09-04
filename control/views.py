from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import DetailView
from django_tables2 import SingleTableView
from .models import Host
from .tables import HostTable
from .ipmi import rmcp

def index(request):
    hostData = {}
    for host in Host.objects.all():
        hostData[host] = rmcp.chassisStatus(host.connection(), host.port, host.cred.username, host.cred.password)
    template = loader.get_template('control/index.html')
    context = {'hostData': hostData}
    return render(request, 'control/index.html', context)

class HostView(DetailView):
    model = Host
    template_name = 'control/host_detail.html'
    
class HostList(SingleTableView):
    model = Host
    table_class = HostTable
    template = 'control/host_list.html'

