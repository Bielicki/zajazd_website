from django.forms import CheckboxInput
from .models import Client


class ClientFormProcessor:
    def __init__(self, form_list, request):
        self.form_list = form_list
        self.request = request
        self.form = None
        self.existing_client = None

        if 'existing_client' in self.request.session:
            self.existing_client = Client.objects.get(id=self.request.session['existing_client'])
            del self.request.session['existing_client']
    def form_check(self):
        """
        Check which form is passed in request.POST
        Then
        """

        for form in self.form_list:
            non_checkbox_fields = [field for field in form().fields
                                   if form().fields[field].widget.__class__.__name__ != CheckboxInput.__name__]
            for field in non_checkbox_fields:
                if field not in self.request.POST:
                    break
                else:
                    if self.existing_client:
                        self.form = form(data=self.request.POST, instance=self.existing_client)
                    else:
                        self.form = form(data=self.request.POST)
                    return
    #
    # def store_post_data(self):
    #     """
    #     Stores all request.POST data in session
    #     """
    #
    #     for field in self.form.fields:
    #         if field in self.request.POST:
    #             self.request.session[field] = self.request.POST[field]
    #         else:
    #             self.request.session[field] = False

    def process_form(self,):
        if self.form.is_valid():
            if 'email_check' in self.request.POST:
                if Client.objects.filter(email=self.request.POST['email_check']).exists():
                    client = Client.objects.get(email=self.request.POST['email_check'])
                    self.request.session['existing_client'] = client.id
                    return self.form.next_step(instance=client)
                else:
                    return self.form.next_step(initial={'email': self.request.POST['email_check']})
            else:
                client = self.form.save()
                self.request.session['client'] = client.id
                return None
        else:
            return self.form
