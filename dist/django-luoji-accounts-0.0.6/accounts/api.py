from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (Transfer, Account)


@api_view()
def transfer_detail(request, user_id):
    query_account = Account.objects.get_seller_account(user_id=user_id)
    transfer_details = Transfer.objects.get_transfer_details_by_account(query_account)

    list_group = list()
    for transfer_detail in transfer_details:
        data_set = dict()
        time = transfer_detail.time_created
        description = transfer_detail.description

        change = '+' + str(transfer_detail.amount) if transfer_detail.destination == query_account else '-' + str(transfer_detail.amount)
        balance = transfer_detail.destination_balance if transfer_detail.destination == query_account else transfer_detail.source_balance

        data_set['time'] = time
        data_set['description'] = description
        data_set['change'] = change
        data_set['balance'] = balance
        list_group.append(data_set)

    return Response({'details': list_group})
