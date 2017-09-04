from django.views.generic import ListView
from django.shortcuts import render
from django.views import View

from .models import About


class Index(View):
    def get(self, request):
        return render(request, 'index/index.html')


class AboutUs(ListView):
    model = About
    template_name = 'index/about.html'
    context_object_name = 'abouts'


class Contact(View):
    def get(self, request):
        return render(request, 'index/contact.html')