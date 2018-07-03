# -*- coding: utf-8 -*-
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from . import models


# Create your views here.
def index(request):
    return render(request, 'satellite/index.html', {})


def tm(request):
    return render(request, 'satellite/tm.html', {})


def errors(request):
    error_list = models.EventErrComm.objects.all()
    paginator = Paginator(error_list, 2)
    page = request.GET.get('page')
    try:
        e = paginator.page(page)
    except PageNotAnInteger:
        e = paginator.page(1)
    except EmptyPage:
        e = paginator.page(paginator.num_pages)
    return render(request, 'satellite/event_error.html', {'errors': e})


def hello(request):
    hello_list = models.HelloComm.objects.all()
    paginator = Paginator(hello_list, 2)
    page = request.GET.get('page')
    try:
        e = paginator.page(page)
    except PageNotAnInteger:
        e = paginator.page(1)
    except EmptyPage:
        e = paginator.page(paginator.num_pages)
    return render(request, 'satellite/event_error.html', {'errors': e})