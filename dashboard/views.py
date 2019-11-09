from django.views.generic import TemplateView
from django.urls import reverse_lazy
from . util_function import get_global_context

# Create your views here
class IndexView(TemplateView):
    name = 'index'
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(get_global_context())
        return context