# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-13 17:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitu_backend', '0006_auto_20160408_2046'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelTable(
            name='customuser',
            table=None,
        ),
    ]