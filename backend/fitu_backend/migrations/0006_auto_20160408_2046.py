# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-08 20:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitu_backend', '0005_auto_20160406_2255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='auth_user',
        ),
    ]