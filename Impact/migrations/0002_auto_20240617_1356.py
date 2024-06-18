# Generated by Django 3.2.19 on 2024-06-17 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Impact', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('faculte', models.BooleanField(default=True)),
                ('nombre_secteur', models.IntegerField(default=1)),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculties', to='Impact.university')),
            ],
            options={
                'unique_together': {('name', 'university')},
            },
        ),
        migrations.CreateModel(
            name='Filiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filieres', to='Impact.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('matricule', models.BigIntegerField(unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telephone', models.BigIntegerField(unique=True)),
                ('current_year', models.IntegerField(default=1)),
                ('filieres', models.ManyToManyField(related_name='students', to='Impact.Filiere')),
            ],
        ),
        migrations.CreateModel(
            name='UE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('year', models.IntegerField()),
                ('semester', models.IntegerField()),
                ('filiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ues', to='Impact.filiere')),
            ],
            options={
                'unique_together': {('name', 'filiere')},
            },
        ),
        migrations.CreateModel(
            name='StudentYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('academic_year', models.CharField(default='2019-2020', max_length=20)),
                ('admitted', models.BooleanField(default=False)),
                ('filiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_years_filieres', to='Impact.filiere')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_years', to='Impact.student')),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sectors', to='Impact.faculty')),
            ],
            options={
                'unique_together': {('name', 'faculty')},
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, max_digits=6)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='Impact.student')),
                ('ue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='Impact.ue')),
            ],
        ),
        migrations.AddField(
            model_name='filiere',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filieres', to='Impact.sector'),
        ),
        migrations.AlterUniqueTogether(
            name='filiere',
            unique_together={('name', 'faculty')},
        ),
    ]