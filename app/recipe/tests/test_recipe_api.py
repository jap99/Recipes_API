# to test our upload image feature - tempfile (with python to generate temp files)
import tempfile 
# for checking if files exist on the system & creating paths
import os
# our Pillow requirement - lets us create test images to upload to our API 
from PIL import Image 
from django.contrib.auth import get_user_model
from django.test import TestCase 
from django.urls import reverse 
from rest_framework import test, status
from rest_framework.test import APIClient
from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')
# requires the id of the recipe we want to get the details of 
# ---- /api/recipe/recipes
# ---- /api/recipe/recipes/1/
def create_recipe_detail_url(recipe_id):
    # the name of the url the router will create for the viewset
        # you can pass in a list of arguments into the reverse method
    return reverse('recipe:recipe-detail', args=[recipe_id])

def create_upload_image_url(recipe_id):
    # will need to recipe id to upload an image so we'll need to pass it to the reverse function 
        # recipe-upload-image is the name we'll give our endpoint
    return reverse('recipe:recipe-upload-image', args=[recipe_id])




""" CREATE SETUP FUNCTIONS """

def create_sample_tag(user, name='Main Course'):
    """ Create and return sample tag """
    return Tag.objects.create(user=user, name=name)

def create_sample_ingredient(user, name='Cinnamon'):
    """ Create and return sample ingredient """
    return Ingredient.objects.create(user=user, name=name)

# **params passes the argument into a dictionary
def create_sample_recipe(user, **params):
    # .update -- since we'll need many recipes that have multiple params we'll create the following dictionary
    defaults = {
        'title': 'sample recipe',
        'time_minutes': 10,
        'price': 4.00
    }
    defaults.update(params)
    # ** has the reverse effect here than it does above
    r = Recipe.objects.create(user=user, **defaults)
    return r




""" PUBLIC RECIPE API TESTS """

class PublicRecipeAPITests(TestCase):

    def setUp(self):
        self.client = APIClient() 

    def test_that_auth_is_required_to_create_a_recipe(self):
        res = self.client.get(RECIPES_URL) 
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)




""" PRIVATE RECIPE API TESTS """

class PrivateRecipeAPITests(TestCase):

    def setUp(self):
        self.client = APIClient() 
        self.user = get_user_model().objects.create_user(
            'javid@cleandev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_get_list_of_recipes(self):
        create_sample_recipe(user=self.user)
        create_sample_recipe(user=self.user)
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        # pass reciptes to serializer as a list (many)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # assert the data in the response is that same as the data passed to the serializer
        self.assertEqual(res.data, serializer.data)

    def test_only_the_users_recipes_are_retrieved(self):
        user2 = get_user_model().objects.create_user(
            'other@cleandev.com',
            'passowrd2'
        )
        create_sample_recipe(user=user2)
        create_sample_recipe(user=self.user)
        res = self.client.get(RECIPES_URL) 
        recipes = Recipe.objects.filter(user=self.user)
        # pass the list of recipes to the serializer
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # we expect to only get 1 recipe in the list
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
        
    def test_you_can_view_a_recipes_details(self):
        recipe = create_sample_recipe(user=self.user)
        # add a tag and ingredient to the recipe
            # this is how you add an item to a many to many field
                # we won't pass in a name; just use the sample name
        recipe.tags.add(create_sample_tag(user=self.user))
        recipe.ingredients.add(create_sample_ingredient(user=self.user))
        # generate the url we'll call --- creates URL for the recipe we pass in
        url = create_recipe_detail_url(recipe.id)
        res = self.client.get(url)
        # we expect it to be serialized - create one & pass in our response
            # serialize a single object
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_partial_update_on_recipe(self):
        """ Test with PATCH """
        recipe = create_sample_recipe(user=self.user)
        recipe.tags.add(create_sample_tag(user=self.user))
        # get ready to replace the tag
        new_tag = create_sample_tag(user=self.user, name='Curry')
        payload = {'title': 'CTM', 'tags': [new_tag.id] }
        url = create_recipe_detail_url(recipe.id)
        self.client.patch(url, payload)
        # retrieve the updated value from the database
        # need to refresh
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        # get all the tags linked to the recipe
        tags = recipe.tags.all()
        # there should only be one tag
        self.assertEqual(len(tags), 1)
        # the new tags should be in the tags we retrieved
        self.assertIn(new_tag, tags)

    def test_full_update_on_recipe(self):
        """ Test with PUT """
        # if you exclude fields in the payload; those excluded fields won't be in the db when you update the db
        recipe = create_sample_recipe(user=self.user)
        recipe.tags.add(create_sample_tag(user=self.user))
        payload = {'title': 'Spaghetti Carbonara', 'time_minutes': 25, 'price': 5.00 }
        url = create_recipe_detail_url(recipe.id)
        self.client.put(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])
        # check the tags assigned length is zero 
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)



""" IMAGE TESTS """

class RecipeImageUploadTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('user@cleandev.com', 'testpass123')
        self.client.force_authenticate(self.user)
        self.recipe = create_sample_recipe(user=self.user)

    def tearDown(self):
        # makes sure our file system's kept clean after our tests, removes all test files we create, & removes images
        self.recipe.image.delete()

    def test_uploading_valid_image_to_recipe_succeeds(self):
        url = create_upload_image_url(self.recipe.id)
        # create a named temp file on the system that we can write to at a random location (usually in the /temp)
            # (we'll write an image to that file, then we'll upload via HTTP POST)
            # then give it a suffix (aka the extension we want to use)
                # add 'as ntf' else it'll return a file without a name but we want one so we can create one so we can
                    # pass it to our upload_to function of the Recipe's image property
                        # then, when you're out of the 'with' aka the context manager it'll auto. remove that file
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            # just create a black square 10 x 10 pixels
            img = Image.new('RGB', (10, 10))
            # save to the ntf file, in jpg format
            img.save(ntf, format='JPEG')
            # seeking will be done to the end of the file, so if you were to start reading you'd start reading at the end of the file
            # seek sets a pointer to the beginning of the file
            ntf.seek(0)
            # tell django we want to make a multipart form request - aka a form that consists of data (by default it's a form that consists of json)
            res = self.client.post(url, {'image': ntf}, format='multipart')
        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # ensure the image is in the response (the path to the image should be accessible)
        self.assertIn('image', res.data)
        # ensure the path assigned to the image exists in the file system 
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_uploading_bad_image_is_not_uploaded_successfully(self):
        url = create_upload_image_url(self.recipe.id)
        # pass in something other than an image
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)