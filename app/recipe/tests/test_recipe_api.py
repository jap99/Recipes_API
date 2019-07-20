from django.contrib.auth import get_user_model
from django.test import TestCase 
from django.urls import reverse 
from rest_framework import test, status
from rest_framework import APIClient
from core.models import Recipe 
from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')

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
        
