# Generated by Django 4.2 on 2023-05-05 14:35

import datetime
from django.db import migrations, models
import django.db.models.deletion
from doctors import models as md


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0003_alter_doctor_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='title_image_link',
        ),
        migrations.AddField(
            model_name='article',
            name='publish_date',
            field=models.DateField(default="2023-05-05"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='publisher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='doctors.doctor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='doctor',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 5, 17, 35, 19, 477267), null=True),
        ),
    ]