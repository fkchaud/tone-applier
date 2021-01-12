from random import randint

from django.views.generic import FormView

from divine_office.models import Text
from lilypond.builder import build_chant
from lilypond.forms import ApplyToTextForm


class ApplyToTextView(FormView):
    form_class = ApplyToTextForm
    template_name = "lilypond/insert_text.html"

    def form_valid(self, form: ApplyToTextForm):
        text = self.request.POST.get('text')
        tone = self.request.POST.get('tone')
        chant = Text(contents=text)
        file_name = f'file_{randint(0,999999)}.ly'

        result = build_chant(chant, file_name, tone)

        return self.render_to_response(
            self.get_context_data(
                form=form,
                files=result['files'],
            ),
        )
