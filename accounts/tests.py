# -*- coding: utf-8 -*-
from django.test import TestCase
from accounts.models import Account, GeneralAccountManager, Transfer, Transaction
from decimal import Decimal as D

# Create your tests here.


class AccountsTestCase(TestCase):
    fixtures = ['account_details.json']

    def test_create_and_get_sub_account(self):
        # 大平台买家人民币全设备子账户
        buyer = GeneralAccountManager().get_or_create_sub_account(
            '10000', 'BUYER', 'PLATFORM', 'ALL', 'CNY')
        self.assertEquals(buyer.account_number, '100300900010000')

        a = GeneralAccountManager().get_sub_account(
            '10000', 'BUYER', 'PLATFORM', 'ALL', 'CNY')
        self.assertEquals(buyer, a)

    def test_sub_account_quantity(self):
        # 总账户号由 账户类型 和 用户ID 构成。
        GeneralAccountManager().get_or_create_sub_account(
            '10000', 'BUYER', 'PLATFORM', 'ALL', 'CNY')
        GeneralAccountManager().get_or_create_sub_account(
            '10000', 'BUYER', 'PLATFORM', 'WEB', 'JCC')
        GeneralAccountManager().get_or_create_sub_account(
            '10000', 'BUYER', 'IGET', 'ALL', 'CNY')
        GeneralAccountManager().get_or_create_sub_account(
            '10000', 'BUYER', 'IGET', 'IOS', 'CNY')
        GeneralAccountManager().get_or_create_sub_account(
            '10000', 'BUYER', 'LIVE', 'ANDROID', 'JCC')

        quantity = Account.objects.get(
            account_number='10900010000').sub_account_quantity

        self.assertEquals(quantity, 5)


class TransferTestCase(TestCase):
    fixtures = ['accounts.json']

    def setUp(self):
        self.buyer = GeneralAccountManager().get_or_create_sub_account(
            '10000', 'BUYER', 'PLATFORM', 'ALL', 'CNY')
        self.seller = GeneralAccountManager().get_or_create_sub_account(
            '10001', 'SELLER', 'PLATFORM', 'ALL', 'CNY')

    def test_balance(self):
        self.assertEquals(self.buyer.balance, D('0.00'))
        self.assertEquals(self.seller.balance, D('0.00'))
        self.buyer.balance = D('10.00')
        self.buyer.save()
        self.assertEquals(self.buyer.balance, D('10.00'))

    def test_transfer(self):
        self.buyer.balance = D('10.00')
        self.buyer.save()
        self.assertEquals(self.buyer.balance, D('10.00'))

        Transfer.objects.create_transfer(
            self.buyer, self.seller, D('5.00'), self.buyer)

        self.assertEquals(self.buyer.balance, D('5.00'))
        self.assertEquals(self.seller.balance, D('5.00'))

        t1 = Transaction.objects.get(sub_account=self.buyer)
        t2 = Transaction.objects.get(sub_account=self.seller)

        self.assertEquals(t1.amount, D('-5.00'))
        self.assertEquals(t2.amount, D('5.00'))
