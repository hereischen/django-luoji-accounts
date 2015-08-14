# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_number', models.CharField(help_text='\u603b\u8d26\u6237\u7f16\u53f7', unique=True, max_length=128)),
                ('user_id', models.CharField(help_text='\u7528\u6237id', max_length=128)),
                ('time_created', models.DateTimeField(help_text='\u8d26\u6237\u521b\u5efa\u65f6\u95f4', auto_now_add=True)),
                ('status', models.CharField(default=b'OPEN', help_text='\u8d26\u6237\u72b6\u6001', max_length=32, choices=[(b'OPEN', b'\xe5\xbc\x80\xe5\x90\xaf'), (b'FROZEN', b'\xe5\x86\xbb\xe7\xbb\x93'), (b'CLOSED', b'\xe5\x85\xb3\xe9\x97\xad')])),
                ('sub_account_quantity', models.IntegerField(help_text='\u5b50\u8d26\u6237\u6570\u76ee')),
            ],
            options={
                'verbose_name': 'account',
                'verbose_name_plural': 'accounts',
            },
        ),
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_type_en', models.CharField(help_text='\u82f1\u6587\u8d26\u6237\u7c7b\u578b', max_length=128)),
                ('account_type_cn', models.CharField(help_text='\u4e2d\u6587\u8d26\u6237\u7c7b\u578b', max_length=128)),
                ('mapping_code', models.CharField(help_text='\u6620\u5c04\u7f16\u53f7', unique=True, max_length=32)),
            ],
            options={
                'verbose_name': 'account type',
                'verbose_name_plural': 'account types',
            },
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_type_en', models.CharField(help_text='\u82f1\u6587\u8bbe\u5907\u7c7b\u578b', max_length=128)),
                ('device_type_cn', models.CharField(help_text='\u4e2d\u6587\u8bbe\u5907\u7c7b\u578b', max_length=128)),
                ('mapping_code', models.CharField(help_text='\u6620\u5c04\u7f16\u53f7', unique=True, max_length=32)),
            ],
            options={
                'verbose_name': 'device type',
                'verbose_name_plural': 'device types',
            },
        ),
        migrations.CreateModel(
            name='SubAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_number', models.CharField(help_text='\u5b50\u8d26\u6237\u7f16\u53f7', unique=True, max_length=169)),
                ('user_id', models.CharField(help_text='\u7528\u6237id', max_length=128)),
                ('time_created', models.DateTimeField(help_text='\u8d26\u6237\u521b\u5efa\u65f6\u95f4', auto_now_add=True)),
                ('currency', models.CharField(default=b'CNY', help_text='\u4ea4\u6613\u5e01\u79cd', max_length=8, choices=[(b'CNY', b'\xe4\xba\xba\xe6\xb0\x91\xe5\xb8\x81'), (b'JCC', b'\xe8\x8a\x82\xe6\x93\x8d\xe5\xb8\x81')])),
                ('balance', models.DecimalField(default=Decimal('0.000000'), help_text='\u8d26\u6237\u4f59\u989d', null=True, max_digits=12, decimal_places=6)),
                ('status', models.CharField(default=b'OPEN', help_text='\u8d26\u6237\u72b6\u6001', max_length=32, choices=[(b'OPEN', b'\xe5\xbc\x80\xe5\x90\xaf'), (b'FROZEN', b'\xe5\x86\xbb\xe7\xbb\x93'), (b'CLOSED', b'\xe5\x85\xb3\xe9\x97\xad')])),
                ('account', models.ForeignKey(related_name='sub_accounts', to='accounts.Account')),
            ],
            options={
                'verbose_name': 'sub account',
                'verbose_name_plural': 'sub accounts',
            },
        ),
        migrations.CreateModel(
            name='SystemCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sys_code_en', models.CharField(help_text='\u82f1\u6587\u7cfb\u7edf\u4ee3\u7801', max_length=128)),
                ('sys_code_cn', models.CharField(help_text='\u4e2d\u6587\u7cfb\u7edf\u4ee3\u7801', max_length=128)),
                ('mapping_code', models.CharField(help_text='\u6620\u5c04\u7f16\u53f7', unique=True, max_length=32)),
            ],
            options={
                'verbose_name': 'system code',
                'verbose_name_plural': 'system codes',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=12, decimal_places=6)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('sub_account', models.ForeignKey(related_name='transactions', to='accounts.SubAccount')),
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
                ('destination', models.ForeignKey(related_name='destination_transfers', to='accounts.SubAccount')),
                ('source', models.ForeignKey(related_name='source_transfers', to='accounts.SubAccount')),
            ],
            options={
                'verbose_name': 'transfer',
                'verbose_name_plural': 'transfers',
            },
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
