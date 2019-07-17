# import the user serializer we created
    # also import the AuthTokenSerializer
from user.serializers import UserSerializer, AuthTokenSerializer

# We'll use the create api view that comes with django rest_framework 
#   - lets us easily make an API that creates an object in the db that uses the serializer we'll provide
from rest_framework import generics, authentication, permissions

# if we're authenticating with standard method username and pw we can pass the ObtainAuthToken view to our URLs
    # since we're customizing it slightly, we need to import it into our views, extend it with a class, & modify some of the class variables
from rest_framework.authtoken.views import ObtainAuthToken

# import our API settings
from rest_framework.settings import api_settings



# Create a view for our create_user API

class CreateUserView(generics.CreateAPIView):

    # need a class variable that point to the UserSerializer class; SERIALIZER'S USED TO CREATE THE OBJECT
    serializer_class = UserSerializer # that's all we need to do for the view
        # rest_framework - makes it ez to create API that does standard behavior
        #   aka (creating objects in the database)

    # Side note: next - before accessing the api we need to create a URL and wire it to our view
    



class CreateTokenView(ObtainAuthToken):
    """Create new auth token for user"""
    # set our serializer class
    serializer_class = AuthTokenSerializer
    # set our renderer class so we can view the endpoint in the browser
        # so you can type in un and pw in Chrome for example
        # if you don't use this tool you'll need another (like curl) to make the POST request
        # import api_settings; use default ones
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    # side note - next: add url to user/urls.py



class ManagerUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    # class variables for auth. (we'll use token auth.) and permission (just need to be logged in)
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    # add a get_object function to our api view
        # usually you link a model to a view to get the instance of the model
            # in this case we'll override the get_object and just return the auth. user

    def get_object(self):
        """Retrieve and return authenticated user"""
        # when the get object is called, the request will have the user attached to it because of the auth. classes,
            # which takes care of getting the authenticated user and assigning it to the request - django rest_framework feature
        return self.request.user 