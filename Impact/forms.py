from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "placeholder": "Ex: admin@uac.bj",
            "class": "form-control",
            "id": "email",
            "required": True,
        }
    ), label="email")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "votre mot de passe",
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

    sigle = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Ex: EPAC",
            "class": "form-control",
            "id": "facultySigle",
            "required": True,
        }
    ), label="sigle")

    isFaculte = forms.IntegerField(widget=forms.RadioSelect(
        choices=[(0, 'Faculté'), (1, 'École')],
        attrs={
            "class": "form-check-input",
            "id": "isFaculty",
        }
    ), initial=0, label="isFaculte")

    nombre_secteur = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            "placeholder": "Nombre de secteur",
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
                self.fields[f'secteur_{i}_name'] = forms.CharField(
                    label=f'Nom du secteur {i + 1}', 
                    widget=forms.TextInput(attrs={
                        "placeholder": "ex : UCAO Parakou ou secteur industriel",
                        "class": "form-control",
                        "required": True
                    })
                )
                self.fields[f'nombre_filieres_{i}'] = forms.IntegerField(
                    label=f'Nombre de filières pour le secteur {i + 1}',
                    initial=1,
                    widget=forms.NumberInput(attrs={
                        "placeholder": "Nombre de filière dans ce secteur",
                        "class": "form-control",
                        "id": f"nombre_filieres_{i}",
                        "required": True,
                        "min": "1"
                    })
                )

                nombre_filieres = int(self.data.get(f'nombre_filieres_{i}', 0))
                for j in range(nombre_filieres):
                    self.fields[f'filiere_{i}_{j}_name'] = forms.CharField(
                        label=f'Nom de la filière {j + 1} pour le secteur {i + 1}', 
                        widget=forms.TextInput(attrs={
                            "class": "form-control",
                            "placeholder": "Nom de la filière",
                            "required": True
                        })
                    )
                    self.fields[f'filiere_{i}_{j}_sigle'] = forms.CharField(
                        label=f'Sigle de la filière {j + 1} pour le secteur {i + 1}', 
                        widget=forms.TextInput(attrs={
                            "class": "form-control",
                            "placeholder": "Ex: GIT",
                            "required": True
                        })
                    )

        else:
            self.fields['nombre_filieres'] = forms.IntegerField(
                label='Nombre de filières',
                initial=1,
                widget=forms.NumberInput(attrs={
                    "class": "form-control",
                    "placeholder": "Nombre de filière",
                    "id": "nombre_filieres",
                    "required": True,
                    "min": "1"
                })
            )
            nombre_filieres = int(self.data.get('nombre_filieres', 0))
            for i in range(nombre_filieres):
                self.fields[f'filiere_{i}_name'] = forms.CharField(
                    label=f'Nom de la filière {i + 1}', 
                    widget=forms.TextInput(attrs={
                        "class": "form-control",
                        "placeholder": "Nom de la filière",
                        "required": True
                    })
                )
                self.fields[f'filiere_{i}_sigle'] = forms.CharField(
                    label=f'Sigle de la filière {i + 1}', 
                    widget=forms.TextInput(attrs={
                        "class": "form-control",
                        "placeholder": "Ex: GIT",
                        "required": True
                    })
                )

    def clean(self):
        cleaned_data = super().clean()

        faculte = self.faculte

        if faculte.nombre_secteur > 1:
            for i in range(faculte.nombre_secteur):
                nombre_filieres = cleaned_data.get(f'nombre_filieres_{i}', 0)
                for j in range(nombre_filieres):
                    cleaned_data[f'filiere_{i}_{j}_name'] = self.cleaned_data.get(f'filiere_{i}_{j}_name')
                    cleaned_data[f'filiere_{i}_{j}_sigle'] = self.cleaned_data.get(f'filiere_{i}_{j}_sigle')
        else:
            nombre_filieres = cleaned_data.get('nombre_filieres', 0)
            for i in range(nombre_filieres):
                cleaned_data[f'filiere_{i}_name'] = self.cleaned_data.get(f'filiere_{i}_name')
                cleaned_data[f'filiere_{i}_sigle'] = self.cleaned_data.get(f'filiere_{i}_sigle')

        return cleaned_data

class AddFiliereForm(forms.Form):
    name = forms.CharField(
        label='Nom de la filière', 
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Nom de la filière",
            "id": "filiereName",
            "required": True
        })
    )
    
    sigle = forms.CharField(
        label='Sigle de la filière', 
        widget=forms.TextInput(attrs={
            "id": 'filiereSigle',
            "class": "form-control",
            "placeholder": "Ex: GIT",
            "required": True
        })
    )
    
    name_sector = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Nom du secteur",
            "class": "form-control",
            "id": "sectorName",
            "required": True,
        }
    ), label="sectorName")