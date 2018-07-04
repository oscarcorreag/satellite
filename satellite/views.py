# -*- coding: utf-8 -*-
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from . import models


NUM_OBJECTS_PAGE = 50


# Create your views here.
def index(request):
    return render(request, 'satellite/index.html', {})


def tm(request):
    return render(request, 'satellite/tm.html', {})


def errors(request):
    error_list = models.EventErrComm.objects.all()
    paginator = Paginator(error_list, NUM_OBJECTS_PAGE)
    page = request.GET.get('page')
    try:
        e = paginator.page(page)
    except PageNotAnInteger:
        e = paginator.page(1)
    except EmptyPage:
        e = paginator.page(paginator.num_pages)
    return render(request, 'satellite/errors.html', {'info': e})


def hello(request):
    hello_list = models.HelloComm.objects.all()
    paginator = Paginator(hello_list, NUM_OBJECTS_PAGE)
    page = request.GET.get('page')
    try:
        e = paginator.page(page)
    except PageNotAnInteger:
        e = paginator.page(1)
    except EmptyPage:
        e = paginator.page(paginator.num_pages)
    return render(request, 'satellite/hello.html', {'info': e})


def housekeeping(request):
    housek_list = models.HouseKeepComm.objects.all()
    paginator = Paginator(housek_list, NUM_OBJECTS_PAGE)
    page = request.GET.get('page')
    try:
        e = paginator.page(page)
    except PageNotAnInteger:
        e = paginator.page(1)
    except EmptyPage:
        e = paginator.page(paginator.num_pages)
    return render(request, 'satellite/housekeeping.html', {'info': e})
