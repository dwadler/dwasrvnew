from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render


def no_root_page(request):
    print(f"**** request of root page **** request: {request}")
    return HttpResponseNotFound("404")


@login_required
def start_page(request):
    return render(request, 'home/start_page.html')
