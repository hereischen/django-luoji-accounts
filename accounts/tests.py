from django.test import TestCase
from accounts.models import Account

from jccoin.account_wrapper import AudioAccountManager


# Create your tests here.
class AccountsTestCase(TestCase):
    fixtures = ['accounts.json']

    def test_get_or_create_buyer_account_for_audio_android(self):
        ba = AudioAccountManager().get_or_create_buyer_account_for_android(
            '10001000')
        self.assertEquals(ba.account_number, '100401910001000')

    # def test_get_or_create_buyer_account_for_audio_ios(self):
    #     bi = AudioAccountManager().get_or_create_buyer_account_for_ios(
    #         '100010')
    #     self.assertEquals(bi.account_number, '100402100010')

    # def test_get_or_create_seller_account_for_audio_android(self):
    #     sa = AudioAccountManager().get_or_create_seller_account_for_android(
    #         '100010')
    #     self.assertEquals(sa.account_number, '110401100010')

    # def test_get_or_create_seller_account_for_audio_ios(self):
    #     si = AudioAccountManager().get_or_create_seller_account_for_ios(
    #         '100010')
    #     self.assertEquals(si.account_number, '110402100010')

    # def test_sub_account_quantity(self):

    #     AudioAccountManager().get_or_create_buyer_account_for_android(
    #         '100010')
    #     AudioAccountManager().get_or_create_buyer_account_for_ios(
    #         '100010')
    #     AudioAccountManager().get_or_create_seller_account_for_android(
    #         '100010')
    #     AudioAccountManager().get_or_create_seller_account_for_ios(
    #         '100010')

    #     b_quantity = Account.objects.get(
    #         account_number='10100010').sub_account_quantity
    #     a_quantity = Account.objects.get(
    #         account_number='11100010').sub_account_quantity

    #     self.assertEquals(2, b_quantity)
    #     self.assertEquals(2, a_quantity)

    # def test_get_or_create_intermediary_account_for_audio(self):
    #     ia = AudioAccountManager(
    #     ).get_or_create_intermediary_account_for_android()
    #     ii = AudioAccountManager(
    #     ).get_or_create_intermediary_account_for_ios()
    #     self.assertEquals(ia.account_number, '510401999999999')
    #     self.assertEquals(ii.account_number, '510402999999999')

    #     quantity = Account.objects.get(
    #         account_number='51999999999').sub_account_quantity

    #     self.assertEquals(quantity, 2)

    def test_get_or_create_cost_account_for_audio(self):
        ia = AudioAccountManager(
        ).get_or_create_cost_account_for_android()
        ii = AudioAccountManager(
        ).get_or_create_cost_account_for_ios()
        self.assertEquals(ia.account_number, '520401999999999')
        self.assertEquals(ii.account_number, '520402999999999')

        quantity = Account.objects.get(
            account_number='52999999999').sub_account_quantity

        self.assertEquals(quantity, 2)

    # def test_get_or_create_guarantee_account_for_audio(self):
    #     ia = AudioAccountManager(
    #     ).get_or_create_guarantee_account_for_android()
    #     ii = AudioAccountManager(
    #     ).get_or_create_guarantee_account_for_ios()
    #     self.assertEquals(ia.account_number, '530401999999999')
    #     self.assertEquals(ii.account_number, '530402999999999')

    #     quantity = Account.objects.get(
    #         account_number='53999999999').sub_account_quantity

    #     self.assertEquals(quantity, 2)

    # def test_get_or_create_income_account_for_audio(self):
    #     ia = AudioAccountManager(
    #     ).get_or_create_income_account_for_android()
    #     ii = AudioAccountManager(
    #     ).get_or_create_income_account_for_ios()
    #     self.assertEquals(ia.account_number, '540401999999999')
    #     self.assertEquals(ii.account_number, '540402999999999')

    #     quantity = Account.objects.get(
    #         account_number='54999999999').sub_account_quantity

    #     self.assertEquals(quantity, 2)

    # def test_get_or_create_fronzenfund_account_for_audio(self):
    #     ia = AudioAccountManager(
    #     ).get_or_create_fronzenfund_account_for_android()
    #     ii = AudioAccountManager(
    #     ).get_or_create_fronzenfund_account_for_ios()
    #     self.assertEquals(ia.account_number, '550401999999999')
    #     self.assertEquals(ii.account_number, '550402999999999')

    #     quantity = Account.objects.get(
    #         account_number='55999999999').sub_account_quantity

    #     self.assertEquals(quantity, 2)

    # def test_get_or_create_gift_account_for_audio(self):
    #     ia = AudioAccountManager(
    #     ).get_or_create_gift_account_for_android()
    #     ii = AudioAccountManager(
    #     ).get_or_create_gift_account_for_ios()
    #     self.assertEquals(ia.account_number, '560401999999999')
    #     self.assertEquals(ii.account_number, '560402999999999')

    #     quantity = Account.objects.get(
    #         account_number='56999999999').sub_account_quantity

    #     self.assertEquals(quantity, 2)

    # # def test_can_not_get_buyer_account_for_android(self):
    # #     a = AudioAccountManager().get_buyer_account_for_android('100010')
    # #     self.assertIsInstance(a, Exception)

    # def test_can_get_buyer_account_for_android(self):
    #     AudioAccountManager().get_or_create_buyer_account_for_android(
    #         '100010')
    #     ba = AudioAccountManager().get_buyer_account_for_android(
    #         '100010')

    #     self.assertEquals(ba.account_number, '100401100010')
    #     self.assertEquals(ba.balance, D('0.000000'))
