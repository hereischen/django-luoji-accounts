# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150727_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='user_id',
            field=models.CharField(
                default='1234567', help_text='\u7528\u6237id', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subaccount',
            name='user_id',
            field=models.CharField(
                default='1234567', help_text='\u7528\u6237id', max_length=128),
            preserve_default=False,
        ),
    ]
