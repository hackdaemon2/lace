from django.db import models
from django.urls import reverse
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, mobile_number, first_name, last_name, password=None):
        """This function creates the user account"""
        user = self.model(
            mobile_number=mobile_number,
            first_name=first_name,
            last_name=last_name,
            password=password,
        ) 
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, mobile_number, first_name, last_name, password=None):
        """This function creates the super user account"""
        user = self.create_user(
            mobile_number=mobile_number,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )        
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)        
        return user

class User(AbstractBaseUser):
    """User model to store user data.
    
    I am overriding most of the fields in the AbstractBaseUser class
    to set their config to my application's specific tastes"""  
    
    # gender status fields
    MALE = 'M'
    FEMALE = 'F'
    
    GENDER = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )
    
    # profile verification fields
    PENDING = 'P'
    UNVERIFIED = 'U'
    VERIFIED = 'V'
    
    PROFILE_VERIFICATION = (
        (PENDING, _('Pending')),
        (UNVERIFIED, _('Unverified')),
        (VERIFIED, _('Verified'))
    )

    mobile_number = models.CharField(
        null=False, 
        unique=True, 
        max_length=11, 
        blank=False
    )
    password = models.CharField(
        max_length=255, 
        blank=False, 
        null=False
    )
    first_name = models.CharField(
        max_length=50, 
        blank=False, 
        null=False
    )
    last_name = models.CharField(
        max_length=50, 
        blank=False, 
        null=False
    )
    is_active = models.BooleanField(
        null=False, 
        default=False
    )
    profile_verified = models.CharField(
        null=False, 
        default=UNVERIFIED,
        choices=PROFILE_VERIFICATION,
        max_length=15
    )
    is_admin = models.BooleanField(
        null=False, 
        default=False
    )
    is_staff = models.BooleanField(
        null=False, 
        default=False
    )
    bio_data = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        default=None
    )
    nickname = models.CharField(
        max_length=50,
        null=True,
        blank=False,
        default=None
    )
    gender = models.CharField( 
        choices=GENDER, 
        default=MALE,
        max_length=15
    )
    confirmation_code = models.CharField(
        max_length=6,
        null=True,
        blank=False,
        default=None
    )
    nationality = models.ForeignKey(
        to='dashboard.Country', 
        on_delete=models.CASCADE,
        null=True,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True, 
        editable=False
    )
    last_login = models.DateTimeField(
        auto_now=True, 
        editable=True
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'mobile_number'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
    def get_fullname(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_short_name(self):
        return self.email
    
    def __str__(self):
        return self.get_fullname().title()
        
    def get_absolute_url(self):
        return reverse('auth:user_details', kwargs={'pk':self.id})
    
class UserPhoto(models.Model):
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE
    )
    image = models.ImageField( 
        upload_to='image_uploads'
    ) 
    description = models.CharField(
        max_length=255    
    )
    date_uploaded = models.DateTimeField(
        auto_now_add=True, 
        editable=False
    )
    is_active = models.BooleanField(
        null=False, 
        default=False
    )
    is_profile_image = models.BooleanField(
        null=False, 
        default=False
    )
    
    def __str__(self):
        return f'{self.image} ({self.description})'
    
    class Meta:
        db_table = 'user_photos_tbl'
    
class ProfileCompletionProgress(models.Model):
    # profile completion progress fields
    NEW_USER = '0'
    MOBILE_VERIFIED = '1'
    LOCATION_DETAILS_COMPLETED = '2'
    PROFILE_COMPLETED = '3'
    
    PROFILE_COMPLETION_PROGRESS = (
        (NEW_USER, 'New User'),
        (MOBILE_VERIFIED, 'Mobile Verified'),
        (LOCATION_DETAILS_COMPLETED, 'Location Complete'),
        (PROFILE_COMPLETED, 'Profile Completed')
    )
    user = models.OneToOneField(
        to=User, 
        on_delete=models.CASCADE
    )
    profile_completion_progress = models.CharField( 
        choices=PROFILE_COMPLETION_PROGRESS,
        default=NEW_USER,
        max_length=1
    ) 
    created_at = models.DateTimeField(
        auto_now_add=True, 
        editable=False
    )
    updated_at = models.DateTimeField( 
        auto_now=False, 
        editable=True
    )

    class Meta:
        db_table = 'profile_completion_progress_tbl'
