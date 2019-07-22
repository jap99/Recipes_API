# to add custom actions to your viewset
from rest_framework.decorators import action 
# for returning a custom response
from rest_framework.response import Response 
# the views we'll create is from a combination of generic view set & model mixin
    # we're going to base it off the generic view set
        # specifically, we'll use the list model mixin
        # we're able to pull in different parts of a view for our app
            # we only want the LIST function (not create, update, or delete functions)
    # import 'status' to generate a status for our custom action (i'm adding this for uploading the image to a recipe)
from rest_framework import viewsets, mixins, status
# to auth. the requests
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# import the tag and the serializer
from core.models import Tag, Ingredient, Recipe
from recipe import serializers



""" RECIPE VIEWS """

class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
     # add the authentication & permission classes 
    # requires that token auth. is used
    authentication_classes = (TokenAuthentication,)
    # requires that the user's auth. to use the api
    permission_classes = (IsAuthenticated,)

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
        """ Create a new object """
        # now we can pass in whatever mods. we want to do in our create process
        # we'll save & set the user to the authenticated user:
        serializer.save(user=self.request.user)

# create our viewset
    # mixinsCreateModelMixin - adds the CREATE option // override the perform_create so you can assign
        # the tag to the correct user
class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    # add the query set so when we're defining a list model mixin in the generic view set we
    # need to provide the query set we want to return 
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer 
    
# mixing.ListModelMixing -- support for listing ingredients
class IngredientViewSet(BaseRecipeAttrViewSet):
        """ Manage ingredients in the database """ 
        queryset = Ingredient.objects.all()
        serializer_class = serializers.IngredientSerializer
    # register this viewset with the ROUTER 
        # so we can access the endpoint from the web
 
# we'll allow user to create, update, & view details (not just create and update) so we use the ModelViewSet
class RecipeViewSet(viewsets.ModelViewSet):
    """ Manage recipes in the db """
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # this is an action we're overriding
        # get recipes of the auth. user
        return self.queryset.filter(user=self.request.user) 
    # now, the make our recipe work we need to add it to the URL 

    # the function called to get the serializer class for a particular request; 
    #   you'll use this function to change the serializer class for the different actions available on the RecipeViewSet
    #       There are multiple actions available in the ModelViewSet - ie) List - we just want to return the default, 
    #           Retrieve - we want to return the RecipeDetailSerializer so when we call Retrieve it uses that serializer & not the default one
    def get_serializer_class(self):
        # this is an action we're overriding
        """ Return the correct serializer class """
        # check the self.action class variable 
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        # this is an action we're overriding
        """ Create a new recipe """
        serializer.save(user=self.request.user)
    
    # we can add custom function and define with as actions with the @action decorator
        # pass in the methods your action will accept - POST, PUT, PATCH, GET
            # well let users POST an image to a recipe
        # we'll say this action is for a detail aka specific recipe so we'll only be able to upload images for recipes that already exist
            # and we'll use the detail url that has the ID of the recipe of the URL (so it knows which recipe to upload the img for)
        # and the visible path for URL as url_path - upload-image is the action
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
    # pk = the primary key passed into the view with the URL
        """ Upload image to recipe """
        # gets the object that's accessed based on the id in the URL
        recipe = self.get_object()
        # pass in recipe and data to serializer
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        # validate data
        if serializer.is_valid():
            serializer.save()
            # since we have a recipeImage serializer we can use the save function to save the object (performs save on the Recipe model with the updated data)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
            # serializer data = the serializer object that was uploaded (which is the ID of the recipe & the URL of the image)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        # then update the GET SERIALIZER class function