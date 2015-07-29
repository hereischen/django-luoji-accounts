# -*- coding: utf-8 -*-
import re
import logging
from decimal import Decimal as D

from django.db import models
from django.db.models import Q
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)

ACCOUNT_STATUS = (
    ('OPEN', '开启'),
    ('FROZEN', '冻结'),
    ('CLOSED', '关闭'),
)

CURRENCY = (
    ('CNY', '人民币'),
    ('JCC', '节操币'),
)


class GeneralAccountManager(object):

    """
    项目账户管理通用类
    """

    def _validate_user_id(self, user_id):
        regex = r'^[0-9]{9}$'
        if user_id != '9999':
            if not re.match(regex, user_id):
                raise ValueError(
                    "Invalid user id [%s]. User id must be 9 digits long." % user_id)

    def _generate_account_number(self, user_id, account_type,
                                 sys_code, device_type):
        """
        生成account_number:
        总账户 账户号 = 两位账户类型编码  + user id
        子账户 账户号 = 两位账户类型编码 + 两位系统(项目)类型编码 + 两位设备类型编码 + user id
        """
        # 账户类型编码
        account_code = AccountType.objects.get(
            account_type_en=account_type).mapping_code
        # 系统(项目)类型编码
        system_code = SystemCode.objects.get(
            sys_code_en=sys_code).mapping_code
        # 设备类型编码
        device_code = DeviceType.objects.get(
            device_type_en=device_type).mapping_code

        self._validate_user_id(user_id)

        # 总账户 账户号
        account_number = account_code + user_id

        # 子账户 账户号
        sub_account_number = account_code + system_code + device_code + user_id

        return account_number, sub_account_number

    def _is_account_exist(self, account_number):
        return Account.objects.filter(account_number=account_number)

    def _create_account(self, user_id, account_type,
                        sys_code, device_type):

        account_number = self._generate_account_number(user_id=user_id,
                                                       account_type=account_type,
                                                       sys_code=sys_code,
                                                       device_type=device_type)[0]

        account = Account.objects.create(account_number=account_number,
                                         sub_account_quantity=1,
                                         )
        account.save()
        logger.info('Create account >> %s.' % account)

        return account

    def get_or_create_sub_account(self, user_id, account_type,
                                  sys_code, device_type, currency):

        account_number, sub_account_number = self._generate_account_number(user_id=user_id,
                                                                           account_type=account_type,
                                                                           sys_code=sys_code,
                                                                           device_type=device_type)

        if not self._is_account_exist(account_number):
            # 创建一个新的总账户,并使sub_account_quantity为1
            account = self._create_account(user_id=user_id, account_type=account_type,
                                           sys_code=sys_code, device_type=device_type)

            # 子账户
            sub_account, flg = SubAccount.objects.get_or_create(account_number=sub_account_number,
                                                                currency=currency,
                                                                account=account
                                                                )

            if flg:
                # sub_account.save()
                logger.info('Create sub account >> %s.' % sub_account)
            else:
                logger.info('Get sub account >> %s.' % sub_account)

            return sub_account

        else:
            account = self._is_account_exist(account_number)[0]

            # 子账户
            sub_account, flg = SubAccount.objects.get_or_create(account_number=sub_account_number,
                                                                currency=currency,
                                                                account=account
                                                                )

            # 创建子账户时,总账户的子账户数+1
            if flg:
                # sub_account.save()
                logger.info('Create sub account >> %s.' % sub_account)
                account.sub_account_quantity += 1
                account.save()
                logger.info('Update account >> %s.' % account)
            else:
                logger.info('Get sub account >> %s.' % sub_account)

            return sub_account

    def get_sub_account(self, user_id, account_type,
                        sys_code, device_type, currency):

        _, sub_account_number = self._generate_account_number(user_id=user_id,
                                                              account_type=account_type,
                                                              sys_code=sys_code,
                                                              device_type=device_type)

        return SubAccount.objects.get(account_number=sub_account_number)


class Account(models.Model):
    # 注意账户统一保留小数点后六位
    # 账户编号
    account_number = models.CharField(
        max_length=128, unique=True, help_text=u'总账户编号')

    # 账户创建时间
    time_created = models.DateTimeField(auto_now_add=True, help_text=u'账户创建时间')
    # 账户状态
    status = models.CharField(
        max_length=32, choices=ACCOUNT_STATUS, default='OPEN', help_text=u'账户状态')

    # 自账户数
    sub_account_quantity = models.IntegerField(help_text=u'子账户数目')

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def __unicode__(self):
        return u'Account number: [%s] & sub account quantity is [%d]' % (self.account_number,
                                                                         self.sub_account_quantity)

    def is_open(self):
        return self.status == 'OPEN'

    def is_closed(self):
        return self.status == 'CLOSED'

    def is_frozen(self):
        return self.status == 'FROZEN'


class SubAccount(models.Model):
    account_number = models.CharField(
        max_length=169, unique=True, help_text=u'子账户编号')

    # 账户创建时间
    time_created = models.DateTimeField(auto_now_add=True, help_text=u'账户创建时间')

    # 货币种类
    currency = models.CharField(
        max_length=8, choices=CURRENCY, default='CNY', help_text=u'交易币种')

    # 余额
    balance = models.DecimalField(decimal_places=6, max_digits=12,
                                  default=D('0.000000'), null=True, help_text=u'账户余额')

    # 账户状态
    status = models.CharField(
        max_length=32, choices=ACCOUNT_STATUS, default='OPEN', help_text=u'账户状态')

    account = models.ForeignKey('accounts.Account',
                                related_name='sub_accounts')

    class Meta:
        verbose_name = _('sub account')
        verbose_name_plural = _('sub accounts')

    def __unicode__(self):
        return u'Sub account number: [%s], balance: %s.' % (self.account_number,
                                                            self.balance)

    def is_open(self):
        return self.status == 'OPEN'

    def is_closed(self):
        return self.status == 'CLOSED'

    def is_frozen(self):
        return self.status == 'FROZEN'

    def is_debit_permitted(self, amount):
        """
        Test if the a debit for the passed amount is permitted
        """
        if self.account_number[:2] in ('10', '11',):
            return self.balance >= amount
        return True

    def cal_source_balance(self, amount):
        self.balance -= amount
        return self.balance

    def cal_destination_balance(self, amount):
        self.balance += amount
        return self.balance

    def num_transactions(self):
        return u'num_transactions : [%s]' % self.transactions.all().count()

    def _balance(self):
        aggregates = self.transactions.aggregate(sum=Sum('amount'))
        sum = aggregates['sum']
        return D('0.00') if sum is None else sum

    @property
    def amount_available(self):
        return self.balance

# =====================fixtures are provided in accounts.json===============


class AccountType(models.Model):

    account_type_en = models.CharField(max_length=128, help_text=u'英文账户类型')
    account_type_cn = models.CharField(max_length=128, help_text=u'中文账户类型')
    mapping_code = models.CharField(
        max_length=32, unique=True, help_text=u'映射编号')

    class Meta:
        verbose_name = _('account type')
        verbose_name_plural = _('account types')

    def __unicode__(self):
        return u'Account type :%s, mapping code:[%s]' % (self.account_type_en, self.mapping_code)


class SystemCode(models.Model):

    sys_code_en = models.CharField(max_length=128, help_text=u'英文系统代码')
    sys_code_cn = models.CharField(max_length=128, help_text=u'中文系统代码')
    mapping_code = models.CharField(
        max_length=32, unique=True, help_text=u'映射编号')

    class Meta:
        verbose_name = _('system code')
        verbose_name_plural = _('system codes')

    def __unicode__(self):
        return u'System code:%s, mapping code:[%s]' % (self.sys_code_en, self.mapping_code)


class DeviceType(models.Model):

    device_type_en = models.CharField(max_length=128, help_text=u'英文设备类型')
    device_type_cn = models.CharField(max_length=128, help_text=u'中文设备类型')
    mapping_code = models.CharField(
        max_length=32, unique=True, help_text=u'映射编号')

    class Meta:
        verbose_name = _('device type')
        verbose_name_plural = _('device types')

    def __unicode__(self):
        return u'Device type: %s, mapping code:[%s]' % (self.device_type_en, self.mapping_code)

# =========================================================================


class TransferManager(models.Manager):

    def create_transfer(self, source, destination, amount, description=None):
        self.verify_transfer(source, destination, amount)

        logger.debug('From account [%s : %s] to account [%s : %s], transfer amount: [%s] %s.'
                     % (source.account_number, source.balance,
                        destination.account_number, destination.balance,
                        amount, description))

        transfer = self.get_queryset().create(
            source=source,
            destination=destination,
            amount=amount,
            description=description,
            source_balance=D('0.000000'),
            destination_balance=D('0.000000'),
        )
        transfer.transactions.create(sub_account=source, amount=-amount)
        transfer.transactions.create(sub_account=destination, amount=amount)
        source.cal_source_balance(amount)
        destination.cal_destination_balance(amount)
        source.save()
        destination.save()
        # 存储transfer后的余额
        transfer.source_balance = source.balance
        transfer.destination_balance = destination.balance
        transfer.save()

    def verify_transfer(self, source, destination, amount):
        """
        Test whether the proposed transaction is permitted.  Raise an exception
        if not.
        """
        if amount < 0:
            raise ValueError(u'Debits cannot use a negative amount')
        if not source.is_open():
            raise Exception(u'Source account stauts is not open.')
        if not destination.is_open():
            raise Exception(u'Destination account stauts is not open.')
        if source.account_number == destination.account_number:
            raise Exception(
                u"Source account and destination account cannot be same.")
        if not source.is_debit_permitted(amount):
            raise ValueError(
                u'Account: %s has insufficient Balance.' % source.account_number)

    def get_transfer_details_by_account(self, account):
        return self.get_queryset().filter(Q(source=account) | Q(destination=account)).order_by('-time_created')


class Transfer(models.Model):

    """
    A transfer of funds between two accounts.
    """
    # 转账资金来源方
    source = models.ForeignKey('SubAccount',
                               related_name='source_transfers')
    # 转账资金接受方
    destination = models.ForeignKey('SubAccount',
                                    related_name='destination_transfers')
    # 转账资金来源方的余额
    source_balance = models.DecimalField(decimal_places=6, max_digits=12,
                                         default=D('0.000000'), help_text=u'转账后的来源方余额')
    # 转账资金接收方的余额
    destination_balance = models.DecimalField(decimal_places=6, max_digits=12,
                                              default=D('0.000000'), help_text=u'转账后的接受方余额')

    # 转账金额
    amount = models.DecimalField(decimal_places=6, max_digits=12)

    # 转账描述
    description = models.CharField(max_length=256, null=True)

    # 转账创建时间
    time_created = models.DateTimeField(auto_now_add=True)

    objects = TransferManager()

    class Meta:
        verbose_name = _('transfer')
        verbose_name_plural = _('transfers')

    def __unicode__(self):
        return u"Transfer source: %s, destination: %s" % (self.source, self.destination)

    def delete(self, *args, **kwargs):
        raise RuntimeError("Transfers cannot be deleted")


class Transaction(models.Model):
    # Every transfer of money should create two rows in this table.
    # (1) the debit from the source account
    # (2) the credit to the destination account
    transfer = models.ForeignKey('accounts.Transfer',
                                 related_name='transactions')
    sub_account = models.ForeignKey('accounts.SubAccount',
                                    related_name='transactions')

    # The sum of this field over the whole table should always be 0.
    # Credits should be positive while debits should be negative
    amount = models.DecimalField(decimal_places=6, max_digits=12)
    time_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"Transaction amount: %.6f" % (self.amount)

    class Meta:
        unique_together = ('transfer', 'sub_account')
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')

    def delete(self, *args, **kwargs):
        raise RuntimeError("Transactions cannot be deleted")
