"""THE SERIALIZER IS USED TO CREATE THE OBJECT"""

# this is where we'll store the serializers for our User model/class
    # we'll need to import our get_user_model to access our User model/class
    # authenticate lets us pass in a un and pw to auth.
from django.contrib.auth import get_user_model, authenticate

# import the following translation system if you ever plan on supporting multiple languages
    # messages that would be output to the user's screen would be passed through this system
    # Side Note - to support multiple languages you would also need to add the language file
        # Would support the translation
from django.utils.translation import ugettext_lazy as _

# import the serializers module
from rest_framework import serializers

 

# inherit since we're basing serializer from our model 
    # django has a built in serializer
        # we just specify the fields we want for our serializer 
            # then, db conversion will automatically be done for us
        # also helps with retrieving & creating from the database
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model() 
        # model = the model we base our serializer from
        # the fields to include in the serializer; 
            # aka the ones that'll be converted to & from JSON when we make our HTTP POST request
            # we'll then retrieve it in our view & save it to a model
            # aka (the fields we want accessible to our api - either READ or WRITE)
        fields = ('email', 'password', 'name')
        # fields - aka (the fields we'll accept when creating users) // must update if you need to add or remove fields later
        # allows us to configure a few extra settings in our model serializer
            # will be used to ensure the password's WRITE-ONLY & >= 5 characters
        # for the pw 'field' in 'fields'
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}} 

    # from the django rest_framework documentation; we're overriding the create function
    def create(self, validated_data): 
        """Create a new user with an encrypted password and return it"""
        # call the create_user function in our model since by default it only calls the create function & we want to call create_user model manager function so we know the password's encrypted
        # validated_data is data that's passed into our serializer
            # from the JSON data made in the HTTP POST
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update the pw, setting the pw correctly, and return it"""
        # need to pass in an instance & validated_data arg.
            # instance - the model linked to our model instance linked to our model serializer; will be our User object
            # validated_data - will be the fields that have gone through validation (in Meta) & are ready to update
        # first, remove the pw from validated_data (dictionary pop)
            # must provide a default value in case pw doesn't exist; so we set it to None
            # pop - it's like GET except after it's retrieved we're removing password from the original dictionary
                # unlike GET, we must provide the default value in case 'password' doesn't exist
                # we also leave it as "None" since we give user the option to provide/update their pw
        password = validated_data.pop('password', None)
        # run update on the rest of our validated_data
        user = super().update(instance, validated_data)
        # super().update() calls the ModelSerializer's update function
        #if user provided a pw then set and save it
        if password:
            user.set_password(password)
            user.save()
        return user 
 

# Create our Auth token serializer - for the user auth. object

# based off the django standard serializer module
# add the 'authenticate' module (import it)
class AuthTokenSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
 
    # validate is a method provided to us by django; we're overriding it
    def validate(self, attrs):
        """validate and authenticate user"""
        # retrieve the username and password from the attrs
            # attrs - contains all fields that make up our AuthTokenSerializer (ie - email and password)
        email = attrs.get('email')
        password = attrs.get('password')
        # we can then choose to pass or fail the validation
        # we'll use the 'authenticate' function we imported earlier from django.contrib.auth
            # first argument = the request we want to authenticate
                # we'll pass the request to the correct view
                # when a request is made, the context is passed to the serializer
                    # the context is where we can access the request
            # second argument = username - it's the parameter required to authenticate
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        # check if we didn't get a user, display a message
        if not user:
            # the underscore is for the translation function
            msg = _('Unable to authenticate with provided credentials')
            # raise the error
                # django knows how to handle the error
                    # raises error as code 400 and sends response to user with the message
            raise serializers.ValidationError(msg, code='authentication')

        # set the user in the attributes; which we return
        attrs['user'] = user
        return attrs
        # we're returning 'attrs' because we must whenever we override the 'validate' method once the validation's successful