from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
# import Tag model that we created in the Core directory
from core.models import Ingredient 
# import Tag serializer
from recipe.serializers import IngredientSerializer 


# we'll use default router for ingredients API (so it'll have /list)
INGREDIENTS_URL = reverse('recipe:ingredient-list')




""" PUBLIC TESTS """


class PublicIngredientsAPITests(TestCase):
    """Test the publicly available API"""

    def setUp(self):
        self.client = APIClient()

    def test_that_login_is_required_to_access_endpoint(self):
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)




""" PRIVATE TESTS """

class PrivateIngredientsAPITests(TestCase):
    """Test the private available API - only authorized users allowed to access API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@cleandev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_ingredients_list_is_retrieved_successfully(self):
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Pepper')
        Ingredient.objects.create(user=self.user, name='Salt')

        # get the ingredients, then serialize them, then compare them to the serialized ones
        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_that_only_ingredients_of_the_authenticated_user_are_returned(self):
        user2 = get_user_model().objects.create_user(
            'other@cleadnev.com'
            '123abcd'
        )
        # assign ingredient to non-authenticated user
        Ingredient.objects.create(user=user2, name='Vinegar')
        # assign ingredient to authenticated user
        ingredient = Ingredient.objects.create(user=self.user, name='Salt')
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_successfully_created_ingredient(self):
        # ingredient that was supposed to be created was created
        payload = { 'name': 'cabbage' }
        self.client.post(INGREDIENTS_URL, payload)
        # check ingredient exists
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()
        self.assertTrue(exists)

    def test_un_successfully_created_ingredient(self):
        # ingredient that was not supposed to be created was indeed not created
        payload = { 'name': '' }
        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)