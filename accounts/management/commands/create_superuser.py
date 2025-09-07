from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Create a superuser with phone number'

    def add_arguments(self, parser):
        parser.add_argument('--phone', type=str, help='Phone number for superuser')
        parser.add_argument('--password', type=str, help='Password for superuser')

    def handle(self, *args, **options):
        phone_number = options['phone'] or '+1234567890'
        password = options['password'] or 'admin123'
        
        if User.objects.filter(phone_number=phone_number).exists():
            self.stdout.write(
                self.style.WARNING(f'User with phone number {phone_number} already exists')
            )
            return
        
        User.objects.create_superuser(
            phone_number=phone_number,
            password=password,
            first_name='Admin',
            last_name='User'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created superuser with phone: {phone_number}')
        )
