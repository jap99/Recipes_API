# import the user serializer we created
from user.serializers import UserSerializer

# We'll use the create api view that comes with django rest_framework 
#   - lets us easily make an API that creates an object in the db that uses the serializer we'll provide
from rest_framework import generics 




# Create a view for our create_user API

class CreateUserView(generics.CreateAPIView):

    # need a class variable that point to the UserSerializer class; SERIALIZER'S USED TO CREATE THE OBJECT
    serializer_class = UserSerializer # that's all we need to do for the view
        # rest_framework - makes it ez to create API that does standard behavior
        #   aka (creating objects in the database)

    # before accessing the api we need to create a URL and wire it to our view
    