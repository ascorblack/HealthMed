# Generated by Django 4.2 on 2023-05-02 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('title_image_link', models.CharField(blank=True, default='', null=True)),
                ('text', models.TextField()),
            ],
            options={
                'db_table': 'articles',
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('doctor_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=64, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('firstname', models.CharField(max_length=32)),
                ('lastname', models.CharField(max_length=32)),
                ('surname', models.CharField(default=None, max_length=32, null=True)),
                ('last_login', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'doctors',
            },
        ),
        migrations.CreateModel(
            name='DoctorSpecialization',
            fields=[
                ('specialization_id', models.AutoField(primary_key=True, serialize=False)),
                ('specialization_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'doctors_specializations',
            },
        ),
        migrations.CreateModel(
            name='DoctorSchedule',
            fields=[
                ('schedule_id', models.AutoField(primary_key=True, serialize=False)),
                ('schedule_date', models.DateField()),
                ('schedule_start_time', models.TimeField()),
                ('schedule_end_time', models.TimeField()),
                ('schedule_state', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor')),
            ],
            options={
                'db_table': 'doctors_schedules',
            },
        ),
        migrations.AddField(
            model_name='doctor',
            name='specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='doctors.doctorspecialization'),
        ),
    ]