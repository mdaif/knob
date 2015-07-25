from django.views.generic.base import TemplateView
from django.views.generic import View
from IPython.parallel import Client
from django.http import HttpResponse
import json


class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        try:
            rc = Client()
            context['workers_count'] = len(rc.ids)
        except:
            pass
        return context


class CommandExecutionView(View):
    def post(self, request, *args, **kwargs):
        print("**************")
        print(request.POST)
        print("**************")
        return HttpResponse(json.dumps({'success': True}), content_type='application/json', status=200)

