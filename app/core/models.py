import uuid 
# will use os.path to create a valid path for our file destination
import os 
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# the recommended way to get settings from django's settings.py file
    # can use it to get our auth settings model
from django.conf import settings 
# the three above are required to extend the django user model while using some features that come with it
# we can then create our user manager class (provides the helper functions to create a user or super user)


def create_recipe_image_file_path(instance, filename):
    """ Generate file path for new recipe image """
    # splits name into items separated by a .
    # [-1] return the last item in the list (aka the extension)
    ext = filename.split('.')[-1]
    # makes string, the file name 
    filename = f'{uuid.uuid4()}.{ext}'
    # join it to the destination path we want to store the file 
        # join lets you join 2 strings to create a valid path
    return os.path.join('uploads/recipe', filename)




""" MODEL CLASSES """

class UserManager(BaseUserManager): # subclass of BaseUserManager - will override some functions to handle email address instead of username

    def create_user(self, email, password=None, **extra_fields): # we put None in case we want to create a user that isn't active
        # **extra_fields -- takes any extra functions that are passed in and pass them into extra fields so we can just add any additional
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
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        # adding string representation of the model
        # return what you want the string rep. to be
            # we want it to be the name; as shown in on model test
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name 

class Recipe(models.Model):
    # these fields will be in the table
    # if we remove the user it'll remove the recipes too
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # user can add a link to the recipe (in case it's available online)
     # if you have a char field & you want it optional, use blank=True instead of null so 
        # when you create a new instance that field will be set to a blank string
        # if it's null then you need to check if it's null, blank, or has a value (aka, may be extra complexity to check)
    link = models.CharField(max_length=255, blank=True)
    # you can remove the Ingredient from in between the ' and the other ' and instead just add the class name alone
        # but to do this you would need to have the other classes set up and created in the correct order
            # ie. for this case the Ingredient would need to be created above the Recipe class
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    # don't put () at end of create_recipe_image_file_path because we don't want to call the function; just want to pass a reference to it so it's called when needed by django
    image = models.ImageField(null=True, upload_to=create_recipe_image_file_path)

    def __str__(self):
        return self.title