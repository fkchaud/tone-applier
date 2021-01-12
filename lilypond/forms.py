from django import forms


class ApplyToTextForm(forms.Form):
    tone = forms.ChoiceField(
        label="Seleccione un tono",
        choices=[
            ("tone_1da", "Tone Ida"),
            ("tone_2", "Tone II"),
            ("tone_6", "Tone VI"),
        ],
    )
    text = forms.CharField(
        label="Ingrese un texto",
        widget=forms.Textarea,
    )
