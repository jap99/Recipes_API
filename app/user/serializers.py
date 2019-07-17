# this is where we'll store the serializers for our User model/class
    # we'll need to import our get_user_model to access our User model/class
from django.contrib.auth import get_user_model 

# import the serializers module
from rest_framework import serializers

# inherit since we're basing serializer from our model 
    # django has a built in serializer
        # we just specify the fields we want for our serializer 
            # then, db conversion will automatically be done for us
        # also helps with retrieving & creating from the database
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model() # the model we base our serializer from
        # the fields to include in the serializer; 
            # aka the ones that'll be converted to & from JSON when we make our HTTP POST request
            # we'll then retrieve it in our view & save it to a model
            # aka (the fields we want accessible to our api - either READ or WRITE)
        fields = ('email', 'password', 'name') # aka (the fields we'll accept when creating users) // must update if you need to add or remove fields
        # allows us to configure a few extra settings in our model serializer
            # will be used to ensure the password's WRITE-ONLY & >= 5 characters
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}} # for the pw 'field' in 'fields'


    def create(self, validated_data): # from the django rest_framework documentation; we're overriding the create function
        """Create a new user with an encrypted password and return it"""
        # call the create_user function in our model since by default it only calls the create function & we want to call create_user model manager function so we know the password's encrypted
        # validated_data is data that's passed into our serializer
            # from the JSON data made in the HTTP POST
        return get_user_model().objects.create_user(**validated_data)