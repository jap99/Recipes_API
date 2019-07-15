from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse  # used so we can generate our API url

# rest_framework api helper tools
from rest_framework.test import APIClient # a test client to make requests to our api to check the response

from rest_framework import status # a module that has status codes // makes tests a bit easier to read

# Note - db refreshes after each test; users created in 1 test aren't accessible in another test

# At the beginning of any API tests,
#     add a helper function
#     OR
#     a constant variable for the URL we'll be testing



CREATE_USER_URL = reverse('user:create') # creates the user create url & assigns it to CREATE_USER_URL


# now a helper function to create users for our test
def create_user(**params):  # can pass in many params
    return get_user_model().objects.create_user(**params)



"""TEST CLASS"""
# public tests (unauthenticated - ie: create a user) 
# private tests (authenticated - ie: modify user, change password)

class PublicUserAPITests(TestCase):     # Public tests


    def setUp(self):    # have a single client for all our tests
        self.client = APIClient()





    def test_and_verify_user_is_validated_successfully(self): # passing in valid data
        # 1) sample payload - email, pw, name
        payload = {
            'email': 'test@cleandev.com',
            'password': 'testpass',
            'name': 'Test name - jp'
        }
        # 2) make POST request to self.client & to our URL for creating users
        res = self.client.post(CREATE_USER_URL, payload)
        # 3) test that our outcome is what we expect - (aka. code 201)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED) # the 2nd param is from our status module
        # 4) test the object is created
        user = get_user_model().objects.get(**res.data) # if all work, we know the user was created
        # 5) test our pw is correct
        self.assertTrue(user.check_password(payload['password']))
        # 6) test the pw isn't passed in and returned with the request to avoid security vulnerability
        self.assertNotIn('password', res.data)





    def test_user_not_created_if_already_exists(self): 
        payload = {
            'email': 'test@cleandev.com',
            'password': 'testpass',
        }
        create_user(**payload) # unwind payload into our method with **
        # make request
        res = self.client.post(CREATE_USER_URL, payload)
        # we expect code 400 (ie. bad request because user already exists)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)




# one more test before we implement the API


    def test_password_is_more_than_5_characters_in_length(self):
        payload = {
            'email': 'javid@cleandev.com',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        # make sure the request returns code 400 - bad request
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # ensure the user was not created (it shouldn't have)
        user_exists = get_user_model().objects.filter(
        # filter for any user with that email address - if email exists return true, else return false
        email=payload['email']
        ).exists()
        # we want false to be returned
        self.assertFalse(user_exists)