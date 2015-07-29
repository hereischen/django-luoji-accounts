# django-luoji-accounts


Overview
--------
django-luoji-accounts adds a number of indispensible financial account-related capabilities to your Django application, including:

* Account

* Sub Account

* AccountType

* SystemCode

* DeviceType

* Transfer

* Transaction 

Please note, this app was developed under Django==1.8.2.

Quick Start
-----------
django-luoji-accounts contains a low level account and sub accounts system that you can get up and running right away. 

To install Django-Accounts from PyPI::
```bash
pip install django-luoji-accounts
```
Alternatively, you can also install Django-luoji-Accounts from GitHub::
https://github.com/hereischen/django-luoji-accounts

Add 'accounts' to your INSTALLED_APPS in your settings.py::

```python
INSTALLED_APPS = (
...
'accounts',
...
)
```
Include the django-luoji-accounts URLs in your urls.py::

```python
urlpatterns = patterns(
...
(r'^accounts/', include('accounts.urls')),
...
)
```

To customise for your specific usage, create a wrapper in your project, for example, project/account_wrapper.py, it would be:

```python
from accounts.models import GeneralAccountManager

class AudioAccountManager(GeneralAccountManager):

    """
    音频账户管理类
    """
    def _get_or_create_sub_account_for_jcc(self, user_id, account_type, device_type):
        """
        查询或创建
        """
        return self.get_or_create_sub_account(user_id=user_id,
                                              account_type=account_type,
                                              sys_code='AUDIO',
                                              device_type=device_type,
                                              currency='JCC'
                                              )

    def _get_sub_account_for_jcc(self, user_id, account_type, device_type):
        """
        查询
        """
        return self.get_sub_account(user_id=user_id,
                                    account_type=account_type,
                                    sys_code='AUDIO',
                                    device_type=device_type,
                                    currency='JCC'
                                    )

    def get_or_create_buyer_account_for_android(self, user_id):
        return self._get_or_create_sub_account_for_jcc(user_id,'BUYER', 'ANDROID')

    def get_or_create_cost_account_for_android(self):
        return self._get_or_create_sub_account_for_jcc('9999', 'COST', 'ANDROID')


    def get_buyer_account_for_android(self, user_id):
        return self._get_sub_account_for_jcc(user_id, 'BUYER', 'ANDROID')

    def get_cost_account_for_android(self):
        return self._get_sub_account_for_jcc('9999', 'COST', 'ANDROID')

```

To call the methods :

```python
# import required models e.g.. Account, SubAccount

# import your wrapper e.g. from project/account_wrapper.py
from project.account_wrapper import AudioAccountManager

# query or create an android buyer account 查询或创建安卓买家
# return one if it exists
# create and return one if it does not exist
ba = AudioAccountManager().get_or_create_buyer_account_for_android(
    '100010')

# query an android buyer account 查询安卓买家
# return one if it exists
# arise exceptions if one does not exist
ba2 = AudioAccountManager().get_buyer_account_for_android(
    '100010')

# query or create an android cost account  查询或创建安卓赠送账户
ga = AudioAccountManager().get_or_create_cost_account_for_android()


# query an android cost account 查询安卓赠送账户
ga2 = AudioAccountManager().get_cost_account_for_android()


```


That's it!