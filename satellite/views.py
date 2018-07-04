# -*- coding: utf-8 -*-
import os
from django.core.files.storage import FileSystemStorage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils import timezone
from . import models
from tm_file_manager import TmFileManager

NUM_OBJECTS_PAGE = 50


# Create your views here.
def index(request):
    return render(request, 'satellite/index.html')


def tm(request):
    return render(request, 'satellite/tm.html')


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


def upload_tm(request):
    if request.method == 'POST' and request.FILES['tm_file']:
        tm_file = request.FILES['tm_file']
        file_name = os.path.splitext(tm_file.name)
        tm_file.name = file_name[0] + '.' + timezone.now().strftime("%d%b%Y_%H%M%S") + '.txt'
        fs = FileSystemStorage()
        fs.save(tm_file.name, tm_file)
        fm = TmFileManager()
        fm.process(os.path.join(fs.location, tm_file.name))
    return render(request, 'satellite/upload_tm.html')
