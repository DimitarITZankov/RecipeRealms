# Django command to wait for the database to be available
import time
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_up = False

        while not db_up:
            try:
                self.check(databases=['default'])  # This will attempt a connection
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))