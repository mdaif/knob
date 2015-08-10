from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import HttpResponse
from .forms import TelnetInputForm
from .tasks import configure_batch
import json
import math

NO_OF_WORKERS = 5  # celery workers in action
NO_OF_TASKS = NO_OF_WORKERS * 2


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

        for i in range(ips_length):
            new_list = (form.cleaned_data['ips'][i: i + int(math.ceil(float(ips_length) / NO_OF_TASKS))],
                        form.cleaned_data['commands'])
            params.append(new_list)
        res = configure_batch.chunks(params, NO_OF_TASKS)
        res.delay()
        return HttpResponse(json.dumps({'success': True}), content_type='application/json', status=200)

