"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from app.forms import PatientForm, EmbryoForm, BootstrapAuthenticationForm


def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #form = BootstrapAuthenticationForm(request.POST)
        user = authenticate(username='admin', password='password')
        token = user.auth_token
        # check whether it's valid:
        #if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

        return HttpResponseRedirect('/app/login.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BootstrapAuthenticationForm
        return render(
            request,
            'app/login.html',
            {
                'form':form,
                'title':'Login',

            }
        )


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def patient_data(request):
    """ Renders the Patient form page """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PatientForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PatientForm()

    return render(request, 'app/patient.html', {'form': form})

def embryo_data(request):
    """ Renders the Patient form page """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EmbryoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EmbryoForm()

    return render(request, 'app/embryo.html', {'form': form})
