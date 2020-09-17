import django_tables2 as tables
from .models import Host
from django_tables2.utils import A

def error_format(record):
    return ('bg-red' if record.errors() else '') + ' text-center'

def power_format(record):
    return ('bg-success' if record.online() else 'bg-red') + ' text-center'

class HostTable(tables.Table):
    online = tables.BooleanColumn(yesno='\u23FB,\u23FB', attrs={'td': {'class': power_format}})
    errors = tables.BooleanColumn(yesno ='\u2718,-', attrs={'td': {'class': error_format}})
    name = tables.LinkColumn('host', args=[A('pk')])
    class Meta:
        order_by = 'ip'
        model = Host
        template_name = 'django_tables2/bootstrap.html'
        fields = ('name',
                  'ip',
                  'hostname',
                  'cred',
                  'online',
                  'errors',
                  )
