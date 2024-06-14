from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "placeholder": "E-mail",
            "class": "form-control",
            "id": "email",
            "required": True,
        }
    ), label="email")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "Password",
            "class": "form-control",
            "id": "password",
            "required": True,
        }
    ), label="password")