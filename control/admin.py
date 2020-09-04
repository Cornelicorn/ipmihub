from django.contrib import admin
from .models import Host, Credential
from .forms import CredentialForm

class CredentialAdmin(admin.ModelAdmin):
    form = CredentialForm

admin.site.register(Host)
admin.site.register(Credential, CredentialAdmin)