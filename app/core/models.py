from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# the recommended way to get settings from django's settings.py file
    # can use it to get our auth settings model
from django.conf import settings 
    

# the three above are required to extend the django user model while using some features that come with it

# we can then create our user manager class (provides the helper functions to create a user or super user)

class UserManager(BaseUserManager): # subclass of BaseUserManager - will override some functions to handle email address instead of username

    def create_user(self, email, password=None, **extra_fields): # we put None in case we want to create a user that isn't active
        # **extra_fields -- takes any extra functions that are passed in and pass  them into extra fields so we can just add any additional
            # fields that we use with our user models
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Please provide a valid email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields) # creates a new model.. passes the email first & then any extra fields we add
        user.set_password(password) # the correct way to pass a password
        user.save(using=self._db) # using=self._db <-- the way to do it to support multiple databases but it's good practice to keep it anyway
        return user # returns the user model that was just created

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

 
class User(AbstractBaseUser, PermissionsMixin): # create user model
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True) # we want it unique so only user for one email
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) # determines if the user's active or not - in case deactivated
    is_staff = models.BooleanField(default=False)
    """Assign the user manager to the objects attribute"""
    objects = UserManager()
    USERNAME_FIELD = 'email' # by default the USERNAME_FIELD is username; now it's email



class Tag(models.Model):
    """The tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    # assign the user foreign key
    # will be a foreign key to User object, but instead of addressing the User object directly 
        # we'll use best practice of retrieving auth. user model with 'from django.conf import settings'
        # first arg = the model you want to base the foreign key off of
        # second = specify what happens when to tags when we delete a user (since there's a dependency)
            # if you delete the user just delete the tags also
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.cascade
    )
    
    def __str__(self):
        # adding string representation of the model
        # return what you want the string rep. to be
            # we want it to be the name; as shown in on model test
        return self.name
