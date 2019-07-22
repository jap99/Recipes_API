from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

# create users in our tests
def create_sample_user(email='test@cleandev.com', password='testpass'):
    return get_user_model().objects.create_user(email, password)



class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@javid.com'
        password = 'password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password)) # check_password comes with django

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized - all lower string"""
        email = 'test@Javid.com'
        user = get_user_model().objects.create_user(email, 'password123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user w/o email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'password123')

    def test_create_new_superuser(self):
        """Test creating a new super user"""
        user = get_user_model().objects.create_superuser(
            'test@javid.com',
            'password123'
        )
        self.assertTrue(user.is_superuser) # included as part of PermissionsMixin
        self.assertTrue(user.is_staff)

    def test_tag_is_created_and_converts_to_correct_string_representation(self):
        # create our tag
            # give it a name we may use in our system
        tag = models.Tag.objects.create(
            user=create_sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_the_ingredient_string_representation(self):
        # sample ingredient with the user
        # just verifies that the model exists so we know it's available to be retrieved
        ingredient = models.Ingredient.objects.create(
            user=create_sample_user(),
            name='Salt'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_we_can_create_new_recipe_objects_and_retrieve_them_as_a_string(self):
        recipe = models.Recipe.objects.create(
            user=create_sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    # the path of the method we'll mock, then add it to the params of our test
    @patch('uuid.uuid4')
    def test_image_is_saved_in_correct_location(self, mock_uuid):
        # mock the uuid function 
        # ensure the string created for the path is what we expect it to be & matches the sample uuid
        uuid = 'test-uuid'
        # mock the return value
        # anytime we trigger the uuid4 function that's triggered from here in our test, it'll override the value with 'test-uuid'
            # this lets us reliably test how our function works
        mock_uuid.return_value = uuid 
        # create the function that's called after the test; it will return file path
            # need to create create_recipe_image_file_path() // will accept the instance (required by django, but we'll put none... & the file name of the file we'll add)
                # we'll remove the myimage prefix & replace it with the uuid (but will keep the extension .jpg)
        file_path = models.create_recipe_image_file_path(None, 'myimage.jpg')
        # ensure the path is what we expect it to be
        # make an f string (aka literal string interpolation - can instert variables in your string w/o having to use the . format)
            # you insert variables with {}
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)