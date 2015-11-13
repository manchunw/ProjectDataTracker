from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Login Email', max_length=50)
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput)