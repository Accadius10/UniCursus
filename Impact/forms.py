from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="username")
    password = forms.CharField(widget=forms.PasswordInput, label="password")