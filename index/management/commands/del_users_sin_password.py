import random

from django.core.management.base import BaseCommand, CommandError
from index.models import Person
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = '''
    This command deletes all users without a password. 
    '''

    def add_arguments(self, parser):
        parser.add_argument('n', nargs='*', type=str, default=18, help="""
        The amount of users you want to delete. (default=18)
        You can enter 'all' to delete all users""")

    def handle(self, *args, **options):
        users = Person.objects.all()
        amount = options['n']
        if type(amount) == list:
            amount = amount[0]
            if amount == 'all':
                amount = len(users)
            else:
                amount = int(amount)

        for user in users:
            if amount == 0:
                break
            if not user.has_usable_password():
                self.stdout.write(f'{user.first_name}{user.last_name} AKA {user.username} had no password')
                user.delete()
                amount -= 1
