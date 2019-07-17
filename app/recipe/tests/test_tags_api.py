from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

# import Tag model that we created in the Core directory
from core.models import Tag 

# import Tag serializer
from recipe.serializers import TagSerializer 




# url will be in the recipe app 
    # & we'll be using a view set which auto. appends the action name to the end of url using the Router
# for listing tags
TAGS_URL = reverse('recipe:tag-list') 





"""PUBLIC TESTS"""

class PublicTagsAPITests(TestCase):
    
    """Test the publicly available tags api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_is_required_for_retrieving_tags(self):
        # make unauthorized request to the api 
        res = self.client.get(TAGS_URL)
        # assert it returned status code 401 
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)




"""PRIVATE TESTS"""

class PrivateTagsAPITests(TestCase):
    
    """ Test the authorized user tags API """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@cleandev.com',
            'pass1234'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_tags_are_retrieved(self):
        # make some sample tags
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')
        # make request to our url to get the tags
        res = self.client.get(TAGS_URL)
        # get all tags in reverse alphabetical order by name
        tags = Tag.objects.all().order_by('-name')
        # serialize tags object
            # there will be more than 1 item in our serializer so many=True (we want to serialize the list of objects)
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # assert the response data's equal to the serializer data we passed in
            # tags should also all be in data & in order by name
        self.assertEqual(res.data, serializer.data)

    def test_user_only_retrieves_their_tags(self):
        """Test that tags returned in response are for the authenticated user"""
        # new user so we can assign a tag to it & compare to the user created in setUp() 
            # will verify the new user isn't included in response since he's not the authenticated user
        user2 = get_user_model().objects.create_user(
            'other@user.com',
            'passwordk'
        )
        # create a new tag object (for the new user)
        Tag.objects.create(user=user2, name='Fruity')
        # create a new tag (to assign to the authenticated user)
        tag = Tag.objects.create(user=self.user, name='Comfort Food')
        # make request
            # we'll expect only 1 tag to be returned in the list
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # verify we got the correct amount of tags returned to us; should only be one for this test
            # the length of the array that was returned in the request
        self.assertEqual(len(res.data), 1)
        # test the name of the tag that was returned is the correct name
        self.assertEqual(res.data[0]['name'], tag.name)