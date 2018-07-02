# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import loader
from grids import ExampleGrid


# Create your views here.
def index(request):
    template = loader.get_template('satellite/index.html')
    return HttpResponse(template.render({}, request))


def grid_handler(request):
    # handles pagination, sorting and searching
    grid = ExampleGrid()
    return HttpResponse(grid.get_json(request), content_type="application/json")


def grid_config(request):
    # build a config suitable to pass to jqgrid constructor
    grid = ExampleGrid()
    return HttpResponse(grid.get_config(), content_type="application/json")
