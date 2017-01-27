from django.shortcuts import render

# Create your views here.

def index(req):
    return render(req, 'mainsite/index.html')

def generic(req):
    return render(req, 'mainsite/generic.html')

def elements(req):
    return render(req, 'mainsite/elements.html')