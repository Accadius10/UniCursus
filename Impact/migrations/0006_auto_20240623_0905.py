# Generated by Django 3.2.19 on 2024-06-23 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Impact', '0005_ue_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='sigle',
            field=models.CharField(default='EPAC', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='filiere',
            name='sigle',
            field=models.CharField(default='GIT', max_length=20),
            preserve_default=False,
        ),
    ]