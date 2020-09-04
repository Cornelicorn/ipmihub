from django.views.generic import DetailView
from django_tables2 import SingleTableView
from .models import Host
from .tables import HostTable
from .ipmi import rmcp


class HostView(DetailView):
    model = Host
    template_name = 'control/host_detail.html'
    
class HostList(SingleTableView):
    model = Host
    table_class = HostTable
    template = 'control/host_list.html'

