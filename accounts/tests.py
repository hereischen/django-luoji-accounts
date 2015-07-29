from django.test import TestCase
from accounts.models import Account

from decimal import Decimal as D
from jccoin.account_wrapper import AudioAccountManager


# Create your tests here.
class AccountsTestCase(TestCase):
    fixtures = ['accounts.json']

    def test_get_or_create_buyer_account_for_audio_android(self):
        ba = AudioAccountManager().get_or_create_buyer_account_for_android(
            '100010')
        self.assertEquals(ba.account_number, '100401100010')

    def test_get_or_create_buyer_account_for_audio_ios(self):
        bi = AudioAccountManager().get_or_create_buyer_account_for_ios(
            '100010')
        self.assertEquals(bi.account_number, '100402100010')

    def test_get_or_create_seller_account_for_audio_android(self):
        sa = AudioAccountManager().get_or_create_seller_account_for_android(
            '100010')
        self.assertEquals(sa.account_number, '110401100010')

    def test_get_or_create_seller_account_for_audio_ios(self):
        si = AudioAccountManager().get_or_create_seller_account_for_ios(
            '100010')
        self.assertEquals(si.account_number, '110402100010')

    def test_sub_account_quantity(self):

        AudioAccountManager().get_or_create_buyer_account_for_android(
            '100010')
        AudioAccountManager().get_or_create_buyer_account_for_ios(
            '100010')
        AudioAccountManager().get_or_create_seller_account_for_android(
            '100010')
        AudioAccountManager().get_or_create_seller_account_for_ios(
            '100010')

        b_quantity = Account.objects.get(
            account_number='10100010').sub_account_quantity
        a_quantity = Account.objects.get(
            account_number='11100010').sub_account_quantity

        self.assertEquals(2, b_quantity)
        self.assertEquals(2, a_quantity)

    def test_get_or_create_intermediary_account_for_audio(self):
        ia = AudioAccountManager(
        ).get_or_create_intermediary_account_for_android()
        ii = AudioAccountManager(
        ).get_or_create_intermediary_account_for_ios()
        self.assertEquals(ia.account_number, '5104019999')
        self.assertEquals(ii.account_number, '5104029999')

        quantity = Account.objects.get(
            account_number='519999').sub_account_quantity

        self.assertEquals(quantity, 2)

    def test_get_or_create_cost_account_for_audio(self):
        ia = AudioAccountManager(
        ).get_or_create_cost_account_for_android()
        ii = AudioAccountManager(
        ).get_or_create_cost_account_for_ios()
        self.assertEquals(ia.account_number, '5204019999')
        self.assertEquals(ii.account_number, '5204029999')

        quantity = Account.objects.get(
            account_number='529999').sub_account_quantity

        self.assertEquals(quantity, 2)

    def test_get_or_create_guarantee_account_for_audio(self):
        ia = AudioAccountManager(
        ).get_or_create_guarantee_account_for_android()
        ii = AudioAccountManager(
        ).get_or_create_guarantee_account_for_ios()
        self.assertEquals(ia.account_number, '5304019999')
        self.assertEquals(ii.account_number, '5304029999')

        quantity = Account.objects.get(
            account_number='539999').sub_account_quantity

        self.assertEquals(quantity, 2)

    def test_get_or_create_income_account_for_audio(self):
        ia = AudioAccountManager(
        ).get_or_create_income_account_for_android()
        ii = AudioAccountManager(
        ).get_or_create_income_account_for_ios()
        self.assertEquals(ia.account_number, '5404019999')
        self.assertEquals(ii.account_number, '5404029999')

        quantity = Account.objects.get(
            account_number='549999').sub_account_quantity

        self.assertEquals(quantity, 2)

    def test_get_or_create_fronzenfund_account_for_audio(self):
        ia = AudioAccountManager(
        ).get_or_create_fronzenfund_account_for_android()
        ii = AudioAccountManager(
        ).get_or_create_fronzenfund_account_for_ios()
        self.assertEquals(ia.account_number, '5504019999')
        self.assertEquals(ii.account_number, '5504029999')

        quantity = Account.objects.get(
            account_number='559999').sub_account_quantity

        self.assertEquals(quantity, 2)

    def test_get_or_create_gift_account_for_audio(self):
        ia = AudioAccountManager(
        ).get_or_create_gift_account_for_android()
        ii = AudioAccountManager(
        ).get_or_create_gift_account_for_ios()
        self.assertEquals(ia.account_number, '5604019999')
        self.assertEquals(ii.account_number, '5604029999')

        quantity = Account.objects.get(
            account_number='569999').sub_account_quantity

        self.assertEquals(quantity, 2)

    # def test_can_not_get_buyer_account_for_android(self):
    #     a = AudioAccountManager().get_buyer_account_for_android('100010')
    #     self.assertIsInstance(a, Exception)

    def test_can_get_buyer_account_for_android(self):
        AudioAccountManager().get_or_create_buyer_account_for_android(
            '100010')
        ba = AudioAccountManager().get_buyer_account_for_android(
            '100010')

        self.assertEquals(ba.account_number, '100401100010')
        self.assertEquals(ba.balance, D('0.000000'))
