from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=200, null=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash the password if it's a new object
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, password):
        return check_password(password, self.password)

class Faculty(models.Model):
    name = models.CharField(max_length=150, null=False)
    isFaculte = models.IntegerField(default=1, null=False)
    nombre_secteur = models.IntegerField(default=1)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculties', null=False)

    class Meta:
        unique_together = ('name', 'university')

class Sector(models.Model):
    name = models.CharField(max_length=200, null=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='sectors', null=False)

    class Meta:
        unique_together = ('name', 'faculty')

class Filiere(models.Model):
    name = models.CharField(max_length=250, null=False)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='filieres')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='filieres', null=False)

    class Meta:
        unique_together = ('name', 'faculty')

class UE(models.Model):
    name = models.CharField(max_length=250, null=False)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='ues')
    year = models.IntegerField()
    semester = models.IntegerField()

    class Meta:
        unique_together = ('name', 'filiere')

class Student(models.Model):
    name = models.CharField(max_length=500, null=False)
    matricule = models.BigIntegerField(unique=True ,null=False)
    email = models.EmailField(unique=True ,null=False)
    telephone = models.BigIntegerField(unique=True ,null=False)
    filieres = models.ManyToManyField(Filiere, related_name='students')
    current_year = models.IntegerField(default=1)

class Grade(models.Model):
    ue = models.ForeignKey(UE, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    score = models.DecimalField(max_digits=6, decimal_places=2, null=False)

class StudentYear(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_years')
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='student_years_filieres')
    year = models.IntegerField()
    academic_year = models.CharField(max_length=20, default='2019-2020')
    admitted = models.BooleanField(default=False)

