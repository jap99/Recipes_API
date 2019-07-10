# import the patch function from the unit test . mock module
    # lets us mock the behavior of the django get db method
from unittest.mock import patch

from django.core.management import call_command

#import the error django throws when db is unavailable & will use it to simulate the data being available when we run our command
from django.db.utils import OperationalError

# import our test case
from django.test import TestCase






class CommandTests(TestCase):


    def test_wait_for_db_ready(self):
        """Test what happens when we call our command & db is available"""
        # simulate the behavior of django when db is available
            # our management command will try to get the db connection from django & check for errors
                # if error, db is unavailable

        # override the behavior of our connection handler & make it return true and therefore mgmt cmd will let us continue
        # use the patch to mock the connection handler to just return true each time it's called
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi: # the location of the code being called is in this module: django.db.utils.ConnectionHandler & the method that's called when u retrieve the db is __getitem__
            # when we create our mgmt cmd, the way we test the db is available in django is we try to get the default db via the connection handler
            # mock the behavior of __getitem__ by using the patch; as a variable called 'gi' (like get item)

            # the way u mock the behavior of a function is you just do:
            gi.return_value = True # means that whenever this is called during our test execution, instead of actually performing what's done in line 24, we'll override it and replace it with a mock object to just return true & we'll monitor how many times it was called & the different calls that were made to it

            #test our call command
            call_command('wait_for_db')

            # in assertion, just test the __getitem__ was called once
            self.assertEqual(gi.call_count, 1)
            # we'll simulate the databse being available & not being available for when we test our command




    @patch('time.sleep', return_value=True) # replaces the behavior of time.sleep with a mock function that returns true; so it won't wait during testing
    def test_wait_for_db(self, ts):
        """The wait_for_db command waits 5 times, and will be successful on 6th turn"""
        # when we create our mgmt cmd later, the way it'll work is it will be a while loop that checks to see if the
            # connection handler raises an error. If yes, it'll wait & then try again - so it does flood the output by trying every microsecond
            # we could remove that delay by adding a patch decordator @patch('time.sleep', return_value=True)

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # instead of adding a return value; adding a side effect - part of unit test mock module
                # can add a side effect to the method ur mocking
                    # we'll make it raise an error 5 times but not on the 6th, then call should complete
            gi.side_effect = [OperationalError] * 5 + [True] # raises error for first 5 times; + [True] means no error on 6th
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
