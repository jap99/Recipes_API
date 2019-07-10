# importing time - the default python module that lets our app sleep a few seconds in between each database check
import time

#import the connections module, which we want so we can test if the db connection is available
from django.db import connections

#import the error django will throw if db isn't available
from django.db.utils import OperationalError

# needed so we can build our custom commmand
from django.core.management.base import BaseCommand





# create our command class

class Command(BaseCommand):

    """Django command to pause execution until db is available"""
    # put our code in a handle function that's run whenever we run this mgmt command

    def handle(self, *args, **options): # passing in custom arguments and options to our mgmt command - ie. customize wait time as an option
        # once db is available we'll just exit
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn: # aka, while this is a false value, try to set it to the db connection; if it's unavailable, django raises an error n we show error, then sleeps execution for a second and then tries again
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable; waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database is available!')) # outputs a green output
