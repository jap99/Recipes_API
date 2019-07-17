from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse  # so we can generate our API url
# rest_framework test helper tools
from rest_framework.test import APIClient # a test client to make requests to our api & check the response
from rest_framework import status # module that has status codes // makes tests easier to read

# Note - db refreshes after each test; users created in 1 test aren't accessible in another test
# At the beginning of any API tests, add a helper function OR constant variable for the URL we'll be testing


CREATE_USER_URL = reverse('user:create') # based on the app & URL in urls.py // app = user // will look in the 'user' app for a url called 'create' 
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):  # can pass in many params // dynamic list of args.  # this method is used to easily create a user when the test requires that a user already exists (for example: test_user_exists()).
    return get_user_model().objects.create_user(**params)
   


"""PUBLIC TEST CLASS"""         

class PublicUserAPITests(TestCase):      

    def setUp(self):     
        self.client = APIClient()


# CREATE USER (CREATE_USER_URL)

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


# TOKENS (TOKEN_URL)

    def test_token_was_created_for_user(self):
        payload = {'email': 'test@cleandev.com', 'password': 'testpass'}
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload) 
        # should get status 200 & a token in response
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_not_created_for_invalid_credentials(self):
        create_user(email='javid@cleandev.com', password='testpass')
        payload = {'email': 'javid@cleandev.com', 'password': 'wrongpass'}
        response = self.client.post(TOKEN_URL, payload)
        # since creds in payload were wrong we shouldn't get back a token in the response
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_not_created_for_nonexistant_user(self):
        payload = {'email': 'javid@cleandev.com', 'password': 'testpass'}
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_not_created_if_password_was_not_provided_in_textfield(self):
        response = self.client.post(TOKEN_URL, {'email': 'anthing', 'password': ''})
        # No token should be provided
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# MANAGE USER (ME_URL)

    def test_that_authentication_is_required_for_the_manage_user_endpoint(self):
        """Test that authentication is required for users"""
        response = self.client.get(ME_URL)
        # make sure we get the correct status code for unauthorized request to the endpoint
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)





"""PRIVATE TEST CLASS"""


class PrivateUserAPITests(TestCase):
    
    # only doing authentication in the setup & not each time for each test
    def setUp(self):
        self.user = create_user(
            email='test@cleandev.com',
            password='testpass',
            name='sample name'
        )
        self.client = APIClient()
        # use the force authenticate helper method to auth. any request made with our sample user
        self.client.force_authenticate(user=self.user)

        

    
        # MANAGE USER (ME_URL)

        def test_profile_is_retrieved_successfully(self):
            """Test that profile is retrieved for authenticated user"""
            response = self.client.get(ME_URL)
            # assert status code is 200
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            # test we got back the correct user
            self.assertEqual(response.data, {
                'name': self.user.name,
                'email': self.user.email
            })


        def test_user_profile_is_modified_successfully(self):
            """Test that authenticated user can successfully make changes to their profile"""
            payload = {
                'name': 'new name sample',
                'password': 'newpass1234'
            }
            res = self.client.patch(ME_URL, payload)
            # update the user with the latest values on the db // refresh_from_db() is django method
            self.user.refresh_from_db()
            # assert all the values we provided were updated correctly
            self.assertEqual(self.user.name, payload['name'])
            self.assertTrue(self.user.check_password(payload['password']))
            # assert correct status code
            self.assertEqual(res.status_code, status.HTTP_200_OK)


        def test_POST_request_on_me_url_not_allowed(self):
            res = self.client.post(ME_URL, {})
            # assert for 405 status code
            self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)