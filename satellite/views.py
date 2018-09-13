# -*- coding: utf-8 -*-
import os
from django.utils import dateparse
from django.core.files.storage import FileSystemStorage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils import timezone
from . import models
from tm_file_manager import TmFileManager
import pdb

NUM_OBJECTS_PAGE = 50


# Create your views here.
def index(request):
    return render(request, 'satellite/index.html')


def tm(request):
    return render(request, 'satellite/tm.html')


def errors(request):
    by_year, year = filter_by_year(request)
    by_time_from, time_from = filter_by_time(request, 'post_time_from')
    by_time_to, time_to = filter_by_time(request, 'post_time_to')
    error_list = None
    if by_year:
        error_list = models.EventErrComm.objects.filter(year__eq=year)
    if by_time_from:
        if error_list is None:
            error_list = models.EventErrComm.objects.filter(post_time__gte=time_from)
        else:
            error_list = error_list.filter(post_time__gte=time_from)
    if by_time_to:
        if error_list is None:
            error_list = models.EventErrComm.objects.filter(post_time__lte=time_to)
        else:
            error_list = error_list.filter(post_time__lte=time_to)
    if not by_year and not by_time_from and not by_time_to:
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
    by_year, year = filter_by_year(request)
    by_time_from, time_from = filter_by_time(request, 'post_time_from')
    by_time_to, time_to = filter_by_time(request, 'post_time_to')
    hello_list = None
    if by_year:
        hello_list = models.HelloComm.objects.filter(year__eq=year)
    if by_time_from:
        if hello_list is None:
            hello_list = models.HelloComm.objects.filter(post_time__gte=time_from)
        else:
            hello_list = hello_list.filter(post_time__gte=time_from)
    if by_time_to:
        if hello_list is None:
            hello_list = models.HelloComm.objects.filter(post_time__lte=time_to)
        else:
            hello_list = hello_list.filter(post_time__lte=time_to)
    if not by_year and not by_time_from and not by_time_to:
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
    by_year, year = filter_by_year(request)
    by_time_from, time_from = filter_by_time(request, 'post_time_from')
    by_time_to, time_to = filter_by_time(request, 'post_time_to')
    housek_list = None
    if by_year:
        housek_list = models.HouseKeepComm.objects.filter(year__eq=year)
    if by_time_from:
        if housek_list is None:
            housek_list = models.HouseKeepComm.objects.filter(post_time__gte=time_from)
        else:
            housek_list = housek_list.filter(post_time__gte=time_from)
    if by_time_to:
        if housek_list is None:
            housek_list = models.HouseKeepComm.objects.filter(post_time__lte=time_to)
        else:
            housek_list = housek_list.filter(post_time__lte=time_to)
    if not by_year and not by_time_from and not by_time_to:
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
    msg = ""
    if request.method == 'POST' and request.FILES['tm_file']:
        tm_file = request.FILES['tm_file']
        file_name = os.path.splitext(tm_file.name)
        tm_file.name = file_name[0] + '.' + timezone.now().strftime("%d%b%Y_%H%M%S") + '.txt'
        fs = FileSystemStorage()
        fs.save(tm_file.name, tm_file)
        fm = TmFileManager()
        result = fm.process(os.path.join(fs.location, tm_file.name))
        msg = "File uploaded successfully!"
        if result == -1:
            msg = "File already uploaded!"
    return render(request, 'satellite/upload_tm.html', {'msg': msg})


def filter_by_year(request):
    try:
        year = int(request.GET.get('year'))
    except (ValueError, TypeError):
        return False, -1
    return True, year


def filter_by_time(request, param_name):
    try:
        time_ = dateparse.parse_datetime(request.GET.get(param_name))
        if time_ is None:
            return False, None
    except (ValueError, TypeError):
        return False, None
    return True, time_
