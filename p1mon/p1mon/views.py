from django.shortcuts import render,redirect

# Create your views here.
def home(request):
    context = {}
    return render(request, 'index.html', context=context)# -*- coding: utf-8 -*-

def contact(request):
    context = {}
    return render(request, 'contact.html', context=context)# -*- coding: utf-8 -*-


def redirect_view(request):
    response = redirect('/serialdata/live/elecgas/')
    return response