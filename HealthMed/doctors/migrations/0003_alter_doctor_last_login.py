# Generated by Django 4.2 on 2023-05-04 14:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_alter_doctor_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 4, 17, 54, 25, 448287), null=True),
        ),
    ]