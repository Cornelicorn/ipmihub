from django.forms import ModelForm, PasswordInput, CharField
from .models import Credential

class CredentialForm(ModelForm):
    password = CharField(required = True, widget=PasswordInput())
    class Meta:
        model = Credential
        fields = '__all__'
