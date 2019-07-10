# this is where we store all our admin test_create_new_superuser

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

#add a helper function called reverse - allows us to generate URLs for our django admin page
from django.urls import reverse


class AdminSiteTests(TestCase):

    # runs before any test is runs
    def setUp(self):
        # sets up test client, add a new user to test, ensure user's logged into client, create normal user to login to admin page
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@javid.com',
            password='pw12345'
        )
        # log admin into the client with force_login
        self.client.force_login(self.admin_user) # lets us not have to manually log the user in / can just use the force_login helper
        # create another user that we can use for listening, etc.
        self.user = get_user_model().objects.create_user(
            email='tests@javid.com',
            password='pass1234',
            name='Test user full name'
        )



    # for SUPER USER
    # need to customize django admin to work with our custom user model; default uses a username but we use an email address so we must change admin.py to support our user models
    def test_users_listed(self):
        """Tests the users are logged into django admin & test that users are listed on user page"""
        url = reverse('admin:core_user_changelist') # these urls are defined in the django admin documentation
            # ^generates the url for our list_user page
        res = self.client.get(url) # uses our test client to perform an http GET on the url --- res == response

        self.assertContains(res, self.user.name) # assertContains is a django assertion; checks our response contains something & is code 200
        self.assertContains(res, self.user.email)
