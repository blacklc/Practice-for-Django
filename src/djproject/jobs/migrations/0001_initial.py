# -*- coding: utf-8 -*-
# Generated by Django 1.10rc1 on 2016-08-04 02:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateField()),
                ('job_title', models.CharField(max_length=50)),
                ('job_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Location'),
        ),
    ]
