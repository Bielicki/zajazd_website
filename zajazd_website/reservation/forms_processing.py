from django.forms import CheckboxInput


class ReservationFormProcessor:
    def __init__(self, form_list, request):
        self.form_list = form_list
        self.request = request
        self.form = None
        self.date_from = None
        self.date_to = None

        if 'date_from' in self.request.session and 'date_to' in self.request.session:
            self.date_from = self.request.session['date_from']
            self.date_to = self.request.session['date_to']

        # if 'room' in self.request.session:
        #     self.room = self.request.session['room']

    def form_check(self):
        """
        Check which form is passed in request.POST
        Then return that form
        Notice that I pass multiple args, its because I use inheritance in form classes and I need those arguments to be present during initialization
        """

        for form in self.form_list:
            non_checkbox_fields = [field for field in form().fields
                                   if form().fields[field].widget.__class__.__name__ != CheckboxInput.__name__]
            for field in non_checkbox_fields:
                if field not in self.request.POST:
                    break
                else:
                    self.form = form(self.date_from, self.date_to, self.request.POST)
                    return

    def store_post_data(self):
        """
        Stores all request.POST data in session
        :return:
        """
        for field in self.form.fields:
            if field in self.request.POST:
                self.request.session[field] = self.request.POST[field]
            else:
                self.request.session[field] = False

    def process_form(self,):
        if self.form.is_valid():
            self.store_post_data()
            return self.form.next_step(self.date_from, self.date_to)
        else:
            return self.form
