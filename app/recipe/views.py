# the views we'll create is from a combination of generic view set & model mixin
    # we're going to base it off the generic view set
        # specifically, we'll use the list model mixin
        # we're able to pull in different parts of a view for our app
            # we only want the LIST function (not create, update, or delete functions)
from rest_framework import viewsets, mixins 

# to auth. the requests
from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated

# import the tag and the serializer
from core.models import Tag, Ingredient
from recipe import serializers


# create our viewset
    # mixinsCreateModelMixin - adds the CREATE option // override the perform_create so you can assign
        # the tag to the correct user
class TagViewSet(viewsets.GenericViewSet, 
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    # add the authentication & permission classes 
    # requires that token auth. is used
    authentication_classes = (TokenAuthentication,)
    # requires that the user's auth. to use the api
    permission_classes = (IsAuthenticated,)
    # add the query set so when we're defining a list model mixin in the generic view set we
    # need to provide the query set we want to return 
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        #overriding
        """Return objects for the current authenticated user only""" 
        #By the time the user enters this method we already know they're authenticated 
            # and that an auth. token was used; otherwise they'd get an error
        # When our List function & view set are invoked from a URL, get_queryset is called to retrieve the queryset
            # this is where we can filter to only getting objects for the auth. user
                # whatever's returned is displayed in the API
        # don't do Tag.objects.all(); do queryset in case it's changed
        # the request object should be passed to self as a class variable 
        #   & the user should be assigned since it requires auth.
        return self.queryset.filter(user=self.request.user).order_by('-name')


    # overriding from mixingsCreateModelMixin
    def perform_create(self, serializer):
        """ Create a new tag """
        # now we can pass in whatever mods. we want to do in our create process
        # we'll save & set the user to the authenticated user:
        serializer.save(user=self.request.user)


# mixing.ListModelMixing -- support for listing ingredients
class IngredientViewSet(viewsets.GenericViewSet, 
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
        """ Manage ingredients in the database """
        # class variables
        authentication_classes = (TokenAuthentication,)
        permission_classes = (IsAuthenticated,)
        queryset = Ingredient.objects.all()
        serializer_class = serializers.IngredientSerializer

        # get only the user's ingredients 
            # onrder by name
        def get_queryset(self):
            return self.queryset.filter(user=self.request.user).order_by('-name')

    # register this viewset with the ROUTER 
        # so we can access the endpoint from the web


        def perform_create(self, serializer):
            """ Create new ingredient """
            serializer.save(user=self.request.user) 
            #by now the tests should pass and you should be able to load the endpoint in a browser