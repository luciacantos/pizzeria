import requests
from django.shortcuts import render

def home(request):
    return render(request, 'LittleItaly/home.html')