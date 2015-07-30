# -*- coding:utf-8 -*-
from django.http import HttpResponse

from .models import (Account, Transfer)
# Create your views here.


def get_revenue_and_cost_details_by_account(request, user_id):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print user_id
    query_account = Account.objects.get_seller_account(user_id=user_id)
    transfer_details = Transfer.objects.get_transfer_details_by_account(query_account)
    list_ = list()
    print '|', u'时间'.ljust(10), '|', u'详情'.ljust(10), '|', u'收支'.ljust(10), '|', u'余额'.ljust(10)
    for transfer_detail in transfer_details:
        time = transfer_detail.time_created
        description = transfer_detail.description
        in_or_out = '+' + str(transfer_detail.amount) if transfer_detail.destination == query_account else '-' + str(transfer_detail.amount)
        balance = transfer_detail.destination_balance if transfer_detail.destination == query_account else transfer_detail.source_balance
        list_.append((time, description, in_or_out, balance))
        print '|', str(time).ljust(10), '|', str(description).ljust(10), '|', str(in_or_out).ljust(10), '|', str(balance).ljust(10)

    return HttpResponse('success')
