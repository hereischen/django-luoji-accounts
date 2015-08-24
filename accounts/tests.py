from django.test import TestCase
from accounts.models import Account
from decimal import Decimal as D
from jccoin.account_wrapper import IgetAccountManager


# Create your tests here.
class JCCAccountsTestCase(TestCase):
    fixtures = ['accounts.json']

    def test_get_or_create_buyer_account_for_audio_android(self):
        ba = IgetAccountManager().get_or_create_buyer_account_for_android(
            '10001000')
        self.assertEquals(ba.account_number, '100401910001000')

    def test_get_or_create_buyer_account_for_audio_ios(self):
        bi = IgetAccountManager().get_or_create_buyer_account_for_ios(
            '100010')
        self.assertEquals(bi.account_number, '100402100010')

    def test_get_or_create_seller_account_for_audio_android(self):
        sa = IgetAccountManager().get_or_create_seller_account_for_android(
            '100010')
        self.assertEquals(sa.account_number, '110401100010')

    def test_get_or_create_seller_account_for_audio_ios(self):
        si = IgetAccountManager().get_or_create_seller_account_for_ios(
            '100010')
        self.assertEquals(si.account_number, '110402100010')

    def test_sub_account_quantity(self):

        IgetAccountManager().get_or_create_buyer_account_for_android(
            '100010')
        IgetAccountManager().get_or_create_buyer_account_for_ios(
            '100010')
        IgetAccountManager().get_or_create_seller_account_for_android(
            '100010')
        IgetAccountManager().get_or_create_seller_account_for_ios(
            '100010')

        b_quantity = Account.objects.get(
            account_number='10100010').sub_account_quantity
        a_quantity = Account.objects.get(
            account_number='11100010').sub_account_quantity

        self.assertEquals(2, b_quantity)
        self.assertEquals(2, a_quantity)

    def test_get_or_create_intermediary_account_for_audio(self):
        ia = IgetAccountManager(
        ).get_or_create_intermediary_account_for_android()
        ii = IgetAccountManager(
        ).get_or_create_intermediary_account_for_ios()
        self.assertEquals(ia.account_number, '510401999999999')
        self.assertEquals(ii.account_number, '510402999999999')

        quantity = Account.objects.get(
            account_number='51999999999').sub_account_quantity

        self.assertEquals(quantity, 2)

    def test_get_or_create_cost_account_for_audio(self):
        ia = IgetAccountManager(
        ).get_or_create_cost_account_for_android()
        ii = IgetAccountManager(
        ).get_or_create_cost_account_for_ios()
        self.assertEquals(ia.account_number, '520401999999999')
        self.assertEquals(ii.account_number, '520402999999999')

        quantity = Account.objects.get(
            account_number='52999999999').sub_account_quantity

        self.assertEquals(quantity, 2)

    def test_get_or_create_guarantee_account_for_audio(self):
        ia = IgetAccountManager(
        ).get_or_create_guarantee_account_for_android()
        ii = IgetAccountManager(
        ).get_or_create_guarantee_account_for_ios()
        self.assertEquals(ia.account_number, '530401999999999')
        self.assertEquals(ii.account_number, '530402999999999')

        quantity = Account.objects.get(
            account_number='53999999999').sub_account_quantity

        self.assertEquals(quantity, 2)

    def test_get_or_create_income_account_for_audio(self):
        ia = IgetAccountManager(
        ).get_or_create_income_account_for_android()
        ii = IgetAccountManager(
        ).get_or_create_income_account_for_ios()
        self.assertEquals(ia.account_number, '540401999999999')
        self.assertEquals(ii.account_number, '540402999999999')

        quantity = Account.objects.get(
            account_number='54999999999').sub_account_quantity

        self.assertEquals(quantity, 2)

    def test_get_or_create_fronzenfund_account_for_audio(self):
        ia = IgetAccountManager(
        ).get_or_create_fronzenfund_account_for_android()
        ii = IgetAccountManager(
        ).get_or_create_fronzenfund_account_for_ios()
        self.assertEquals(ia.account_number, '550401999999999')
        self.assertEquals(ii.account_number, '550402999999999')

        quantity = Account.objects.get(
            account_number='55999999999').sub_account_quantity

        self.assertEquals(quantity, 2)

    def test_get_or_create_gift_account_for_audio(self):
        ia = IgetAccountManager(
        ).get_or_create_gift_account_for_android()
        ii = IgetAccountManager(
        ).get_or_create_gift_account_for_ios()
        self.assertEquals(ia.account_number, '560401999999999')
        self.assertEquals(ii.account_number, '560402999999999')

        quantity = Account.objects.get(
            account_number='56999999999').sub_account_quantity

        self.assertEquals(quantity, 2)

    def test_can_get_buyer_account_for_android(self):
        IgetAccountManager().get_or_create_buyer_account_for_android(
            '100010')
        ba = IgetAccountManager().get_buyer_account_for_android(
            '100010')

        self.assertEquals(ba.account_number, '100401100010')
        self.assertEquals(ba.balance, D('0.000000'))
