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

class CreateFacultyForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Nom de la faculté",
            "class": "form-control",
            "id": "facultyName",
            "required": True,
        }
    ), label="name")

    isFaculte = forms.BooleanField(widget=forms.RadioSelect(
        choices=[(True, 'Faculté'), (False, 'École')],
        attrs={
            "class": "form-check-input",
            "id": "isFaculty",
            "required": True,
        }
    ), label="isFaculte")

    nombre_secteur = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            "placeholder": "0",
            "class": "form-control",
            "id": "sectorNmbre",
            "min": "0",
        }
    ), label="nombre_secteur")