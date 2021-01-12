from datetime import datetime

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    TemplateView,
)

from divine_office.connect import get_liturgy
from divine_office.forms import FindLiturgyForm
from lilypond.builder import build_chant


class FindLiturgy(FormView):
    template_name = 'divine_office/index.html'
    form_class = FindLiturgyForm
    success_url = reverse_lazy('show-liturgy')

    def form_valid(self, form: FindLiturgyForm):
        pass


class ShowLiturgyView(TemplateView):
    template_name = "divine_office/show.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        import ipdb; ipdb.set_trace()
        return context


def dummy(request):
    return HttpResponse("Dummy")


# Create your views here.
def index(request):
    today = datetime.now()
    liturgy = get_liturgy(today, 'visperas')
    file_idx = 0

    for chant in liturgy.chants:
        build_chant(chant, f"file_{file_idx}.ly")
        file_idx += 1

    return HttpResponse("Holis")
