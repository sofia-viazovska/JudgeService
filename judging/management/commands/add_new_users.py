from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Adds specified users with surname_firstletter username format'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding new users...')

        # List of users to add (first_name, last_name)
        users_to_add = [
            ('Igor', 'Tkachenko'),
            ('Oleksandr', 'Yosypenko'),
            ('Serhiy', 'Chernikov'),
            ('Mihail', 'Antonishin'),
            ('Yaroslav', 'Melnychenko'),
            ('Vlad', 'Fedenko'),
            ('Andrii', 'Tsabanov'),
            ('Mykola', 'Chyrkov'),
            ('Test', 'Test')
        ]

        for first_name, last_name in users_to_add:
            # Create username in format surname_first letter of name
            username = f"{last_name.lower()}_{first_name[0].lower()}"

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'User {username} already exists'))
                continue

            # Create the user
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=f"{username}@example.com",  # Random email
                password=f"{last_name.lower()}pass"  # Setting a default password
            )

            # Ensure the user is not an admin
            user.is_staff = False
            user.is_superuser = False
            user.save()

            self.stdout.write(self.style.SUCCESS(f'User {username} ({first_name} {last_name}) created successfully'))

        self.stdout.write(self.style.SUCCESS('All users have been added successfully'))
