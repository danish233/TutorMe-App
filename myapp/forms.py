from django import forms

from .models import TutorSession

class TutorSessionForm(forms.ModelForm):
    class Meta:
        model = TutorSession
        fields = "__all__"

