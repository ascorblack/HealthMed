# Generated by Django 4.2 on 2023-05-04 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='status',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
