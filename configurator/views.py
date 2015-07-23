from django.views.generic.base import TemplateView
from IPython.parallel import Client

# Create your views here.
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