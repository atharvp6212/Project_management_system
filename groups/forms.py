from django import forms
from .models import Group
from accounts.models import User
       
class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'mentor']  # Remove members from here

    # This will be used to filter students in the view
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'] = forms.ModelMultipleChoiceField(
            queryset=User.objects.filter(role='student'),
            widget=forms.CheckboxSelectMultiple,
            required=True
        )