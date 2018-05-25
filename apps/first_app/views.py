# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.contrib import messages
from django.shortcuts import render,HttpResponse, redirect

def index(request):
    return render(request, "first_app/index.html")
    
def register(request):
    if request.method == "POST":
        result = User.objects.validate_registration(request.POST)
        if type(result) == list:
            for x in result:
                messages.error(request, x)
                return redirect('/')
        else:
            request.session['id'] = result.id
            request.session['name'] = request.POST['name']
            # request.session['role'] = request.POST['role']
            messages.success(request, 'You have registered successfully!')
            return render(request,"first_app/dashboard.html")

def login(request): 
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for x in result:
            messages.error(request, x)
        return redirect('/')
    else:
        request.session['id'] = result.id
        request.session['name'] = result.name
        # request.session['role'] = result.role
        print 'login success'
        messages.success(request, 'You have logged in!')        
        return render(request,"first_app/dashboard.html")
# Create your views here.
