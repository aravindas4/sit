# Generated by Django 2.1.2 on 2018-10-31 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple', '0002_added password field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='password',
            field=models.CharField(max_length=10000),
        ),
    ]
