from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import HttpResponse
from .forms import TelnetInputForm
from .tasks import configure_batch, email_admin
from celery import chord, group
from knob.celery import app as celery_app
from .helpers import ProgressChord
import json
import math

try:
    stats = celery_app.control.inspect().stats()
    NO_OF_WORKERS = stats[stats.keys()[0]]['pool']['max-concurrency']
except KeyError:
    NO_OF_WORKERS = None


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['workers_count'] = NO_OF_WORKERS

        return context


class CommandExecutionView(View):
    def post(self, request, *args, **kwargs):

        form = TelnetInputForm(request.POST)
        if not form.is_valid():
            return HttpResponse(
                json.dumps({'success': False, 'validation_error': True, 'message': form.errors, 'form_error': True}),
                content_type="application/json", status=200)

        params = []

        ips_length = len(form.cleaned_data['ips'])
        for i in range(0, ips_length, int(math.ceil(float(ips_length) / NO_OF_WORKERS))):
            new_list = (form.cleaned_data['ips'][i: i + int(math.ceil(float(ips_length) / NO_OF_WORKERS))],
                        form.cleaned_data['commands'], form.cleaned_data['username'], form.cleaned_data['password'])

            params.append(new_list)

        configurations = configure_batch.chunks(params, NO_OF_WORKERS)
        progress_chord = ProgressChord(configurations, email_admin.s(form.cleaned_data['admin_email']))
        result = progress_chord.apply_async()

        return HttpResponse(json.dumps({'success': True, 'task_id': result.task_id}),
                            content_type='application/json', status=200)

