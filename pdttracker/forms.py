from django import forms
from .models import *
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput)

class ProjectForm(forms.ModelForm):
    DeveloperList = Group.objects.get(name="Developer").user_set.all()
        
    assign_developer=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=DeveloperList,)
    class Meta:
        model = Project
        fields = ['project_title', 'project_sloc','project_description','current_phase', 'current_iteration', 'assign_developer']

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

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','groups']