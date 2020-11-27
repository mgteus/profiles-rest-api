from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager





# Create your models here.
class UserProfileManager(BaseUserManager):
    """Helps Django works with our custom model"""

    def create_user(self, email, name, password=None):                   #  Password=None means that you dont need a password to use this function
        """Createa new user profile object"""

        if not email:                                                   # "if not" works for blank email or "False" email
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)                             #normalize the email for lowercase letters
        user  = self.model(email=email, name=name)
        user.set_password(password)                                     #set_password encrypts the password and store in the data base with a Hash
        user.save(using=self._db)                                       #saving in db=data base
        return user

    def create_superuser(self, email, name, password):               #Password not None means you need a password to use this function
        """Creates and asves a new super User"""

        user = self.create_user(email, name, password)
        user.is_superuser = True                                        #is_superuser defined by django, it gives the user "powers"
        user.is_staff     = True                                        ##is_staff defined by django, it gives the user "powers"
        user.save(using=self._db)                                       #saving in db=data base

        return user






class UserProfile( AbstractBaseUser, PermissionsMixin):
    """Represents a "UserProfile" inside our system"""
    email       = models.EmailField(max_length=255, unique=True)  #receiving the email from user
    name        = models.CharField(max_length=255)                 #receiving users name
    is_activate = models.BooleanField(default=True)               #Djangos custom models need these lines
    is_staff    = models.BooleanField(default=False)              #              ||

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'                  #Login fields
    REQUIRED_FIELDS = ["name"]


    def get_full_name(self):
        """Used to get users full name"""
        return self.name

    def get_short_name(self):
        """User to get a user short name"""
        return self.name

    def __str__(self):
        """Used to convert the object to a string, django need this"""
        return self.email


class ProfileFeedItem(models.Model):
    """Profile status update."""
    user_profile = models.ForeignKey("UserProfile", on_delete=models.CASCADE)   #Cascade make the api deletes all the information about a user when deleted
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        """Return the model as a string."""

        return self.status_text
