import datetime
import time

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.cache import cache
from django.template.loader import get_template
from django.views import View

from django_kirui.http import response
from django_kirui.utils.paginator import Paginator
from kirui_devserver.backend.forms import SampleForm, FilterForm
from kirui_devserver.backend.models import Activity


def index(request):
    return response(request).from_template('xml/index.html').to_200()


class FormView(View):
    def get(self, request):
        form = SampleForm(request.POST or None, request.FILES or None)
        return response(request).from_template('xml/form.html', context={'form': form}).to_200()

    def post(self, request):
        # print(request.POST, request.FILES)
        form = SampleForm(request.POST or None, request.FILES or None, instance=Activity.objects.first())
        if form.is_valid():
            return response(request).to_340('/backend/index/')
        else:
            return response(request).from_template('xml/form_data.html', {'form': form}).to_403()


def modal(request):
    form = SampleForm(request.POST or None, request.FILES or None)
    form.now = datetime.datetime.now()
    if form.is_valid():
        return HttpResponse('OK')

    if form.is_valid():
        return response(request).from_template('xml/modal.html', context={'form': form}).to_201()
    else:
        return response(request).from_template('xml/modal.html', context={'form': form}).to_403()

    return resp


def table(request):
    data = []
    for row in range(1, 200):
        data.append({'first': f'{row}.1', 'second': f'{row}.2'})

    paginate_to = int(request.GET.get('paginate_to', 1))
    p = Paginator(data, 30)
    page = p.page(paginate_to)

    if request.GET.get('paginate_to', None):
        return response(request).from_template('xml/table_data.html', context={'page': page}).to_201()
    else:
        return response(request).from_template('xml/table.html', context={'page': page}).to_200()


class FilteredTable(View):
    def dispatch(self, request, *args, **kwargs):
        data = []
        for row in range(1, 20):
            data.append({'first': f'{row}.1', 'second': f'{row}.2'})
        self.data = data
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = FilterForm()
        p = Paginator(self.data, 4)
        page = p.page(1)
        return response(request).from_template('backend/filtered_table.html', context={'form': form, 'page': page}).to_200()

    def post(self, request):
        form = FilterForm(request.POST)
        if form.is_valid():
            data = [row for row in self.data if row['first'].startswith(form.cleaned_data['field'])]
        p = Paginator(data, 4)

        paginate_to = int(request.GET.get('paginate_to', 1))
        page = p.page(paginate_to)
        return response(request).from_template('backend/filtered_table_data.html', context={'form': form, 'page': page}).to_201()


def charts(request):
    donut = {'first': 10, 'second': 20, 'third': 30}
    line = {
        'Első': {'Január': 10, 'Február': 20, 'Március': 30},
        'Második': {'Január': 150, 'Február': 15, 'Március': 65}
    }

    return response(request).from_template('backend/charts.html', context={'donut': donut, 'line': line}).to_200()


def card(request):
    return response(request).from_template('backend/card.html', context={}).to_200()


def kanban(request):
    data = {
        'kanban': [
            {'name': 'Stage 1', 'cards': [{'title': 'Card title', 'body': 'Card description', 'link': 'dfsdf'}]},
            {'name': 'Stage 2', 'cards': []},
            {'name': 'Stage 3', 'cards': []},
        ]
    }
    return response(request).from_template('backend/kanban.html', context=data).to_200()
