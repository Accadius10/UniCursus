# Generated by Django 5.0.6 on 2024-06-24 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Impact', '0006_auto_20240623_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='ue',
            name='sigle',
            field=models.CharField(default='UESIGLE', max_length=20),
            preserve_default=False,
        ),
    ]
