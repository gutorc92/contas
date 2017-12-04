from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from subprocess import call, STDOUT
import os
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Prepara o ambiente para testes'

    def db_sqlite_path(self):
        return settings.DATABASES['default']['NAME']

    def manage_path(self):
        return os.path.join(settings.BASE_DIR, "manage.py")

    def is_sqlite(self):
        return "sqlite" in settings.DATABASES['default']['ENGINE']

    def exclude_sqlite(self):
        if (os.path.isfile(self.db_sqlite_path())):
            self.stdout.write("Deleting db")
            call(["rm", self.db_sqlite_path()], stderr=STDOUT)

    def exclude_migrations(self):
        for app in settings.INSTALLED_APPS:
            path_migrations = os.path.join(settings.BASE_DIR,
                                           app, "migrations")
            path_app = os.path.join(settings.BASE_DIR, app)
            if os.path.isdir(path_migrations):
                self.stdout.write("It is going to remove %s" % path_migrations)
                output = call(["rm", "-r", path_migrations], stderr=STDOUT)

            if os.path.isdir(path_app):
                msg = "It will create migrations \
                      {0} {1} {2} {3}".format("python",
                                              self.manage_path(),
                                              "makemigrations",
                                              app)
                self.stdout.write(msg)
                output = call(["python", self.manage_path(),
                               "makemigrations", app], stderr=STDOUT)

    def handle(self, *args, **options):
        self.stdout.write("Prepare command")
        if (self.is_sqlite()):
            self.exclude_sqlite()

        self.exclude_migrations()
        call_command('migrate')
        call_command('loaddata',  "initial")

        
