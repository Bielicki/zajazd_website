from django import forms
from .models import Client


class BaseModelForm(forms.ModelForm):
    def __init__(self, date_from=None, date_to=None, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ClientForm(BaseModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'phone', 'email']


class ClientCheckForm(forms.Form):

    def __init__(self, date_from=None, date_to=None, *args, **kwargs):
        super(ClientCheckForm, self).__init__(*args, **kwargs)
    email_check = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    next_step = ClientForm

client_form_list = [ClientCheckForm,
                    ClientForm]
