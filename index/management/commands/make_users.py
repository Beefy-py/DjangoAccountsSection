import string
import random

from django.core.management.base import BaseCommand, CommandError
from index.models import Person
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = '''
    This command creates (n)users .
    
    *n is the amount you specify as an argument to this command. 
    *The default value of n = 18 if not specified.
    '''

    def add_arguments(self, parser):
        parser.add_argument('n', nargs='*', type=int, default=18)

    def handle(self, *args, **options):
        first_names = []
        last_names = []
        nicknames = []

        with open('c:/users/kenny/Projects/LoginSystem/index/management/commands/first_names.txt', 'r') as file:
            first_names += [i.replace('\n', '') for i in file.readlines() if i.endswith('\n')]

        with open('c:/users/kenny/Projects/LoginSystem/index/management/commands/last_names.txt', 'r') as file:
            last_names += [i.replace('\n', '') for i in file.readlines() if i.endswith('\n')]

        with open('c:/users/kenny/Projects/LoginSystem/index/management/commands/nicknames.txt', 'r') as file:
            nicknames += [i.replace('\n', '') for i in file.readlines() if i.endswith('\n')]

        email_providers = ['@gmail.com',
                           '@hotmail.com',
                           '@outlook.com',
                           '@protonmail.com',
                           '@icloud.com',
                           '@live.com',
                           '@yahoomail.com',
                           '@galaxy.com',
                           ]

        users = []

        amount = options['n']
        if type(amount) == list:
            amount = amount[0]

        nicknames = list(set(nicknames))
        for _ in range(amount):

            username = random.choice(nicknames)
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{random.choice((last_name, username, first_name))}{random.choice((last_name, username, first_name))}{random.choice(email_providers)}".replace(
                ' ', '')

            user_obj = {'username': username,
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email}

            if user_obj not in users:
                users.append(user_obj)

        for user in users:
            try:
                Person.objects.create_user(
                    username=user['username'],
                    first_name=user['first_name'],
                    last_name=user['last_name'],
                    email=user['email'],
                    password=random.choice((None, '12345foo',
                                           ''.join((random.choice(string.printable) for _ in range(20)))))
                )
            except IntegrityError:
                pass
