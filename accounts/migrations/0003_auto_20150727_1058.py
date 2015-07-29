# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150727_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transfer',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='object_id',
        ),
    ]
