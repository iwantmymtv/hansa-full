from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create superusers'

    def handle(self, *args, **kwargs):
        User.objects.create_superuser(username='admin', email='admin@admin.com', password='12345')