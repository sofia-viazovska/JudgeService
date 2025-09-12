from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Updates passwords for all users to follow the consistent format username_password'

    def handle(self, *args, **kwargs):
        self.stdout.write('Updating passwords for all users...')
        
        # Get all non-superuser users
        users = User.objects.filter(is_superuser=False)
        
        updated_count = 0
        for user in users:
            # Set the new password format
            new_password = f"{user.last_name.lower()}pass"
            
            # Update the user's password
            user.set_password(new_password)
            user.save()
            
            updated_count += 1
            self.stdout.write(f"Updated password for user: {user.username}")
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated passwords for {updated_count} users'))
        
        # Print instructions for users
        self.stdout.write("\nPassword format: username_password")
        self.stdout.write("Examples:")
        self.stdout.write("- For user 'tkachenko_i': password is 'tkachenko_i_password'")
        self.stdout.write("- For user 'yosypenko_o': password is 'yosypenko_o_password'")