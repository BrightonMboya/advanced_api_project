from django.shortcuts import redirect
from django.http import HttpResponse


def redirect_to_api(request):
    return redirect('/api/')


def home(request):
    return HttpResponse("<h1>Welcome to the Advanced API Project</h1><p>Go to <a href='/api/'>API</a></p>")
