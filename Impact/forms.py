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

    isFaculte = forms.IntegerField(widget=forms.RadioSelect(
        choices=[(0, 'Faculté'), (1, 'École')],
        attrs={
            "class": "form-check-input",
            "id": "isFaculty",
        }
    ), initial=0, label="isFaculte")

    nombre_secteur = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            "placeholder": "nombre de secteur",
            "class": "form-control",
            "id": "sectorNmbre",
            "min": "1",
        }
    ), initial=1, label="nombre_secteur")

class CreateSecteursFilieresForm(forms.Form):
    def __init__(self, faculte, *args, **kwargs):
        super(CreateSecteursFilieresForm, self).__init__(*args, **kwargs)
        self.faculte = faculte

        if faculte.nombre_secteur > 1:
            for i in range(faculte.nombre_secteur):
                self.fields[f'secteur_{i}_name'] = forms.CharField(label=f'Nom du secteur {i + 1}', required=True)
                self.fields[f'nombre_filieres_{i}'] = forms.IntegerField(label=f'Nombre de filières pour le secteur {i + 1}', required=True)

                nombre_filieres = self.data.get(f'nombre_filieres_{i}', 0)
                for j in range(nombre_filieres):
                    self.fields[f'filiere_{i}_{j}_name'] = forms.CharField(label=f'Nom de la filière {j + 1} pour le secteur {i + 1}', required=True)

        else:
            self.fields['nombre_filieres'] = forms.IntegerField(label='Nombre de filières', required=True)
            nombre_filieres = self.data.get('nombre_filieres', 0)
            for i in range(nombre_filieres):
                self.fields[f'filiere_{i}_name'] = forms.CharField(label=f'Nom de la filière {i + 1}', required=True)

    def clean(self):
        cleaned_data = super().clean()

        faculte = self.faculte

        if faculte.nombre_secteur > 1:
            for i in range(faculte.nombre_secteur):
                nombre_filieres = cleaned_data.get(f'nombre_filieres_{i}', 0)
                for j in range(nombre_filieres):
                    cleaned_data[f'filiere_{i}_{j}_name'] = self.cleaned_data.get(f'filiere_{i}_{j}_name')
        else:
            nombre_filieres = cleaned_data.get('nombre_filieres', 0)
            for i in range(nombre_filieres):
                cleaned_data[f'filiere_{i}_name'] = self.cleaned_data.get(f'filiere_{i}_name')

        return cleaned_data

