#! /usr/bin/env python3

"""Storage your account with AES
Dependence:
- sqlalchemy
- Crypto
- fire
- termcolor
Usage:
- python accountdb add ${YOUR_Account} --username=${USERNAME} --password=${PASSWORD}

or you would like download the releases script accountdb and move it to your bin directory, them
- chmod +x accountdb
- change the DEFAULT_DATABASE_URL to a absolute path like "sqlite:////home/christophe/bin"
- then you can use anywhere with command accountdb
"""

from randomf import Randomf
from aes import AESCipher
from sqlalchemy import Column, String, Binary
from sqlalchemy_toolkit import Base, init_db
from termcolor import colored
import fire

aes_cipher = AESCipher("3.1415926")


class Account(Base):
    __tablename__ = 'account'
    account = Column(String(50), primary_key=True, nullable=False)
    username = Column(String(50))
    password = Column(Binary)
    phone = Column(String(20))
    email = Column(String(50))
    tag = Column(String(500))

    def __repr__(self):
        return (f"ACCOUNT:    {self.account or 'NOTHING'}\n"
                f"USERNAME:   {self.username or 'NOTHING'}\n"
                f"PASSWORD:   {self.decrypt}\n"
                f"PHONE:      {self.phone or 'NOTHING'}\n"
                f"EMAIL:      {self.email or 'NOTHING'}\n"
                f"DETAILS:    {repr(self.tag) if self.tag is not None else 'NOTHING'}")

    @property
    def decrypt(self):
        return aes_cipher.decrypt(self.password)


class AccountDB:
    AES_KEY = ""
    DEFAULT_DATABASE_URL = "sqlite:///account.db"
    session = init_db(DEFAULT_DATABASE_URL)()

    def encrypt(self, raw):
        return aes_cipher.encrypt(raw)

    def add(self, account, username=None, password=None, phone=None, email=None, tag=None):
        new_account = Account(
            account=account,
            username=username,
            password=self.encrypt(password or 'NOTHING'),
            phone=phone,
            email=email,
            tag=tag)
        yes = input(f"{repr(new_account)}\nWould you like to add the account?(y/N):")
        if yes.lower() == 'y':
            self.session.add(new_account)
            self.session.commit()
            return "Add the Account successfully."
        else:
            return "Abort."

    def delete(self, account):
        account = Account.query.filter_by(account=account).first()
        yes = input(colored(f"{repr(account)}\nWARNING:Do you want to delete the account?(y/N):",
                            'red', attrs=["bold"]))
        if yes.lower() == 'y':
            self.session.delete(account)
            self.session.commit()
            return "delete successfully."
        else:
            return "Abort."

    def find(self, account, field=None):
        account = Account.query.filter_by(account=account).first()
        if field == 'password':
            return account.decrypt
        return getattr(account, field) if field is not None else repr(account)

    def find_by(self, username=None, password=None, phone=None, email=None, tag=None):
        kwarg = {}
        if username is not None:
            kwarg["username"] = username
        if password is not None:
            kwarg["password"] = self.encrypt(password)
        if phone is not None:
            kwarg["phone"] = phone
        if email is not None:
            kwarg["email"] = email
        if tag is not None:
            kwarg["tag"] = tag
        accounts = Account.query.filter_by(**kwarg).all()
        return "\n\n".join(map(repr, accounts))

    def modify(self, account, username=None, password=None, phone=None, email=None, tag=None):
        account = Account.query.filter_by(account=account).first()
        yes = input(f"{repr(account)}\nWould you like to modify the account?(y/N):")
        if yes.lower() == 'y':
            account.username = username if username is not None else account.username
            account.password = self.encrypt(password) if password is not None else account.password
            account.phone = phone if phone is not None else account.phone
            account.email = email if email is not None else account.email
            account.tag = tag if tag is not None else account.tag
            self.session.commit()
            return "Modify successfully."
        else:
            return "Abort."

    def gen_random_password(self, length, seed=None):
        result = []
        random = Randomf(seed)
        categories = Randomf.next_int_in_range(0, 3)
        number = Randomf.next_int_in_range(0, 10)
        random_seq, r = random.seq(categories, length)
        for item in random_seq:
            if item == 0:
                s, r = r.next_lower_letter()
                result.append(s)
            elif item == 1:
                s, r = r.next_upper_letter()
                result.append(s)
            else:
                n, r = number(r)
                result.append(str(n))

        return "".join(result)

    def add_with_random_password(self, account, username=None, phone=None, email=None, tag=None):
        new_account = Account(
            account=account,
            username=username,
            password=(self.encrypt(self.gen_random_password(10))),
            phone=phone,
            email=email,
            tag=tag)
        yes = input(f"{repr(new_account)}\nWould you like to add the account?(y/N):")
        if yes.lower() == 'y':
            self.session.add(new_account)
            self.session.commit()
            return "Add the Account successfully."
        else:
            return "Abort."


if __name__ == "__main__":
    fire.Fire(AccountDB)
