from django import forms
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput)

class ProjectForm(forms.ModelForm):
    users= User.objects.all()
        
    assign_member=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=users,)
    class Meta:
        model = Project
        fields = ['project_title', 'project_sloc','project_description','current_phase', 'current_iteration', 'assign_member']

class PhaseForm(forms.ModelForm):
    class Meta:
        model = Phase
        fields = ['phase_name', 'phase_sequence', 'phase_sloc']

class IterationForm(forms.ModelForm):
    class Meta:
        model = Iteration
        fields = ['iteration_name', 'iteration_sequence']


class DefectForm(forms.ModelForm):
    class Meta:
        model = Defect
        fields = ['defect_title', 'defect_type', 'defect_description', 'iteration_injected','defect_remarks' ]