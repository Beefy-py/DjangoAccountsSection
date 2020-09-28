import random

from django.core.management.base import BaseCommand, CommandError
from index.models import Person
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = """
    This command deletes 18 random users from the database.
    TIPS: 
    (1)- passing 'all' deletes all users"""

    def add_arguments(self, parser):
        parser.add_argument('n', type=str, nargs='*', default=18,
                            help='''
                            The number of random users that will be deleted.
                            Default = 18 if n is not specified. 
                            If len(users in database) < 18, nothing happens.
                            ''')

        parser.add_argument('--involved', nargs='*', default=[],
                            help='''Specify space separated user nicknames or user id's.
                            Users with these nicknames will be involved in the deletion process.''')

        parser.add_argument('--skipped', nargs='*', default=[],
                            help='''Specify space separated user nicknames or user id's.
                             Users with these nicknames won't be deleted.''')

    def handle(self, *args, **options):
        if options['n'][0] == 'all':
            for user in Person.objects.all():
                user.delete()
            return self.stdout.write('ALL USERS DELETED!')
        amount = options['n']
        if type(amount) == list:
            amount = int(amount[0])

        users = Person.objects.all()
        users_to_delete = []

        users_involved = options['involved']
        users_to_skip = options['skipped']

        if ''.join(users_to_skip).isdecimal():
            users_to_skip = [Person.objects.get(id=i).username for i in users_to_skip]
            if len(users) >= 18:
                for _ in range(amount):
                    user = random.choice(users)
                    if user.username not in users_to_delete and user.username not in users_to_skip:
                        users_to_delete.append(user)

            elif users_involved and not amount:
                if users_involved[0] == 'all':
                    for i in Person.objects.all():
                        i.delete()
                else:
                    for _id in users_involved:
                        try:
                            user = Person.objects.get(id=_id)
                            user.delete()
                        except ObjectDoesNotExist:
                            raise CommandError(f"User with id {_id} does not exist!")
            else:
                self.stdout.write(self.style.WARNING('No user will be deleted if there are less than 18 users left.'))
        else:
            if len(users) >= 18:
                for _ in range(amount):
                    user = random.choice(users)
                    if user.username not in users_to_delete and user.username not in users_to_skip:
                        users_to_delete.append(user)

            elif users_involved and not amount:
                if users_involved[0] == 'all':
                    for i in Person.objects.all():
                        i.delete()
                else:
                    for nickname in users_involved:
                        try:
                            user = Person.objects.get(username=nickname)
                            user.delete()
                        except ObjectDoesNotExist:
                            raise CommandError(f"{nickname} does not exist!")
            else:
                self.stdout.write(self.style.WARNING('No user will be deleted if there are less than 18 users left.'))

        if ''.join(users_involved).isdecimal():
            _users_involved = []
            for i in users_involved:
                try:
                    _users_involved.append(Person.objects.get(id=i))
                except ObjectDoesNotExist:
                    pass
            users_to_delete += _users_involved
        else:
            if users_involved:
                _users_involved = []
                for i in users_involved:
                    try:
                        _users_involved.append(Person.objects.get(username=i))
                    except ObjectDoesNotExist:
                        pass
                users_to_delete += _users_involved

        errors = 0

        for user in users_to_delete:
            if user not in users_to_skip:
                try:
                    user.delete()
                except AssertionError:
                    errors += 1
        print(f'AssertionErrors: {errors}')
