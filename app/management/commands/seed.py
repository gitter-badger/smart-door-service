import random
from app import models
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate roles, admin and user accounts"

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')

        models.Role.objects.get_or_create(title="user")
        admin_role = models.Role.objects.get_or_create(title="admin")

        if not models.User.objects.filter(username="admin").exists():
            models.User.objects.create_user(
                "admin",
                "admin@example.com",
                "password",
                fullname="Admin",
                role_id=admin_role[0].id
            )

        self.stdout.write('done.')
