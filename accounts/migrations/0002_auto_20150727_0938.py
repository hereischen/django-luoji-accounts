# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=12, decimal_places=6)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'transaction',
                'verbose_name_plural': 'transactions',
            },
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_balance', models.DecimalField(default=Decimal('0.000000'), help_text='\u8f6c\u8d26\u540e\u7684\u6765\u6e90\u65b9\u4f59\u989d', max_digits=12, decimal_places=6)),
                ('destination_balance', models.DecimalField(default=Decimal('0.000000'), help_text='\u8f6c\u8d26\u540e\u7684\u63a5\u53d7\u65b9\u4f59\u989d', max_digits=12, decimal_places=6)),
                ('amount', models.DecimalField(max_digits=12, decimal_places=6)),
                ('description', models.CharField(max_length=256, null=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'transfer',
                'verbose_name_plural': 'transfers',
            },
        ),
        migrations.AlterField(
            model_name='subaccount',
            name='balance',
            field=models.DecimalField(default=Decimal('0.000000'), help_text='\u8d26\u6237\u4f59\u989d', null=True, max_digits=12, decimal_places=6),
        ),
        migrations.AddField(
            model_name='transfer',
            name='destination',
            field=models.ForeignKey(related_name='destination_transfers', to='accounts.SubAccount'),
        ),
        migrations.AddField(
            model_name='transfer',
            name='source',
            field=models.ForeignKey(related_name='source_transfers', to='accounts.SubAccount'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sub_account',
            field=models.ForeignKey(related_name='transactions', to='accounts.SubAccount'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transfer',
            field=models.ForeignKey(related_name='transactions', to='accounts.Transfer'),
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together=set([('transfer', 'sub_account')]),
        ),
    ]
