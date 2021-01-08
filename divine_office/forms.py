from datetime import date


from django import forms


class FindLiturgyForm(forms.Form):
    date = forms.DateField(
        label="Seleccione una fecha",
        initial=date.today,
    )

    liturgy = forms.ChoiceField(
        label="Seleccione una hora",
        choices=[
            ('visperas', 'Vísperas'),
        ],
    )
