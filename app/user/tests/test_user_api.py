from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse  # so we can generate our API url
# rest_framework test helper tools
from rest_framework.test import APIClient # a test client to make requests to our api & check the response
from rest_framework import status # module that has status codes // makes tests easier to read

# Note - db refreshes after each test; users created in 1 test aren't accessible in another test
# At the beginning of any API tests, add a helper function OR constant variable for the URL we'll be testing


CREATE_USER_URL = reverse('user:create') # based on the app & URL in urls.py // app = user // will look in the 'user' app for a url called 'create' 
   
def create_user(**params):  # can pass in many params // dynamic list of args.  # this method is used to easily create a user when the test requires that a user already exists (for example: test_user_exists()).
    return get_user_model().objects.create_user(**params)
   


"""TEST CLASS"""         

class PublicUserAPITests(TestCase):      

    def setUp(self):     
        self.client = APIClient()

    def test_user_is_created_successfully(self):  
        payload = {
            'email': 'test@cleandev.com',
            'password': 'testpass',
            'name': 'Test name - jp'
        } 
        res = self.client.post(CREATE_USER_URL, payload) 
        """User created"""
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)  
        """Correct password"""
        self.assertTrue(user.check_password(payload['password']))   
        """Password not returned in API resonse"""
        self.assertNotIn('password', res.data)                      

    def test_if_user_exists(self): 
        """Don't create duplicate if user already exists"""                                 
        payload = {
            'email': 'test@cleandev.com',
            'password': 'testpass',
        }
        create_user(**payload) # first time creating user  
        res = self.client.post(CREATE_USER_URL, payload) # second time creating user 
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
 
    def test_password_length(self):   
        """Should be greater than 5 characters"""                              
        payload = {
            'email': 'javid@cleandev.com',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)    
        """User not created"""         
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)      
        user_exists = get_user_model().objects.filter( 
        email=payload['email']
        ).exists() 
        """User with that email doesn't exist"""
        self.assertFalse(user_exists)                                       




"""TEST CLASS"""