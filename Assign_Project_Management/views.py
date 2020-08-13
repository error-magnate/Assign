from django.shortcuts import render, redirect
from Application.views import home


def home(request):
    return render(request, 'index.html')