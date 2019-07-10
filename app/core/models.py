from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# import 'abstract base user'
# import 'base user manager'
# import the permissions mix in

# the three above are required to extend the django user model while using some features that come with it

# we can then create our user manager class (provides the helper functions to create a user or super user)

class UserManager(BaseUserManager): # subclass of BaseUserManager - will override some functions to handle email address instead of username

    def create_user(self, email, password=None, **extra_fields): # we put None in case we want to create a user that isn't active
        # **extra_fields -- takes any extra functions that are passed in and pass  them into extra fields so we can just add any additional
            # fields that we use with our user models
        """Creates and saves a new user"""
        user = self.model(email=email, **extra_fields) # creates a new model.. passes the email first & then any extra fields we add
        user.set_password(password) # the correct way to pass a password
        user.save(using=self._db) # using=self._db <-- the way to do it to support multiple databases but it's good practice to keep it anyway

        return user # returns the user model that was just created



class User(AbstractBaseUser, PermissionsMixin): # create user model

    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True) # we want it unique so only user for one email
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) # determines if the user's active or not - in case deactivated
    is_staff = models.BooleanField(default=False)

    """Assign the user manager to the objects attribute"""
    objects = UserManager()

    USERNAME_FIELD = 'email' # by default the USERNAME_FIELD is username; now it's email
