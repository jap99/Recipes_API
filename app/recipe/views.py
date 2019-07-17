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
from core.models import Tag 
from recipe import serializers


# create our viewset
class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
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
