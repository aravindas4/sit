# Generated by Django 2.1.2 on 2018-11-02 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple', '0004_added fields to myuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(default='ash.g.proxy@gmail.com', max_length=30),
        ),
    ]
