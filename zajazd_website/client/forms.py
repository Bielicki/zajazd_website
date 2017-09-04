from django import forms
from .models import Client


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    @classmethod
    def create_form_session(cls, request):
        for field in cls._meta.fields:
            if field == 'breakfast' and field not in request.POST:
                request.session['breakfast'] = False
            else:
                request.session[field] = request.POST[field]

    @classmethod
    def process_form(cls, request):
        if cls(request.POST).is_valid():
            cls.create_form_session(request)
            return {'form': cls.next_step()}
        else:
            return {'form': cls(request.POST)}


class ClientForm(BaseModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'phone', 'email']

    @classmethod
    def process_form(cls, request):
        if 'client' in request.session:
            client = Client.objects.get(id=request.session['client'])
            cls(request.POST, instance=client).save()
            return None
        else:
            if cls(request.POST).is_valid():
                client = cls(request.POST).save()
                request.session['client'] = client.id
            else:
                return {'form': cls(request.POST)}


class ClientCheckForm(forms.Form):
    email_check = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    @classmethod
    def process_form(cls, request):
        if cls(request.POST).is_valid():
            if Client.objects.filter(email=request.POST['email_check']).exists():
                client = Client.objects.get(email=request.POST['email_check'])
                request.session['client'] = client.id
                return {'form': ClientForm(instance=client)}
            else:
                return {'form': ClientForm(initial={'email': request.POST['email_check']})}
        else:
            return {'form': cls(request.POST)}


client_form_list = [ClientCheckForm,
                    ClientForm]
