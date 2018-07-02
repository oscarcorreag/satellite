from jqgrid import JqGrid
from satellite.models import EventErrComm
from django.urls import reverse_lazy


class ExampleGrid(JqGrid):
    model = EventErrComm # could also be a queryset
    fields = ['uid_ev', 'eve_name', 'mis_clock', 'seq_number']  # optional
    url = reverse_lazy('grid_handler')
    # url = "satellite/grid"
    caption = 'My First Grid'  # optional
    colmodel_overrides = {  # optional
        'uid_ev': {'editable': False, 'width': 10},
    }
