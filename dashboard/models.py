from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Create your models here.
class RelationshipStatus(models.Model):
    # relationship status fields
    SINGLE = 'Single'
    MARRIED = 'Married'
    DIVORCED = 'Divorced'
    WIDOWED = 'Widowed'
    OPEN_RELATIONSHIP = 'Open Relationship'
    IN_A_RELATIONSHIP = 'In a Relationship'
    COMPLICATED = 'It is Complicated'
    
    RELATIONSHIP_STATUS = (
        (SINGLE, _('Single')),
        (MARRIED, _('Married')), 
        (DIVORCED, _('Divorced')),
        (WIDOWED, _('Widowed')),
        (OPEN_RELATIONSHIP, _('Open Relationship')),
        (IN_A_RELATIONSHIP, _('In a Relationship')),
        (COMPLICATED, _('It is Complicated')),
    )
    
    # match criteria fields
    LOVE = 'Love'
    FLIRTING = 'Flirting'
    MARRIAGE = 'Marriage'
    
    MATCH_CRITERIA = (
        (LOVE, _('Love')),
        (FLIRTING, _('Flirting')), 
        (MARRIAGE, _('Marriage')),
    )
    
    relationship_status = models.CharField( 
        choices=RELATIONSHIP_STATUS, 
        default=SINGLE,
        max_length=50
    )
    match_criteria = models.CharField(
        choices=MATCH_CRITERIA,
        default=LOVE,
        max_length=50
    )
    user = models.OneToOneField(
        to=get_user_model(), 
        on_delete=models.CASCADE
    ) 
    created_at = models.DateTimeField( 
        auto_now_add=True, 
        editable=False 
    )
    updated_at = models.DateTimeField( 
        auto_now=True, 
        editable=True
    )
    
    class Meta:
        db_table = 'relationship_status_tbl'
     
    
class GenderInterest(models.Model):
     # gender interest fields
    INTERESTED_IN_MEN = 'Interested in Men'
    INTERESTED_IN_WOMEN = 'Interested in Women'
    INTERESTED_IN_BOTH = 'Interested in Men and Women'
    
    GENDER_INTEREST = (
        (INTERESTED_IN_MEN, _('Interested in Men')),
        (INTERESTED_IN_WOMEN, _('Interested in Women')), 
        (INTERESTED_IN_BOTH, _('Interested in Men and Women')),
    )
    
    user = models.OneToOneField(
        to=get_user_model(), 
        on_delete=models.CASCADE
    ) 
    gender_interest = models.CharField( 
        choices=GENDER_INTEREST, 
        default=INTERESTED_IN_BOTH,
        max_length=50
    )
    created_at = models.DateTimeField( 
        auto_now_add=True, 
        editable=False 
    )
    updated_at = models.DateTimeField( 
        auto_now=True, 
        editable=True
    )
    
    class Meta:
        db_table = 'gender_interests_tbl'
        
class Country(models.Model):
    country = models.CharField( 
        max_length=255, 
        blank=True
    )
    created_at = models.DateTimeField( 
        auto_now_add=True, 
        editable=False 
    )
    updated_at = models.DateTimeField( 
        auto_now=True, 
        editable=True
    )
    
    class Meta:
        db_table = 'country_tbl'
           
class SubscriptionLog(models.Model):
    # subscription duration cycles
    MONTHLY = 'Monthly'
    QUARTERLY = 'Quarterly'
    BI_ANNUALLY = 'Bi-Annually'
    ANNUALLY = 'Annually'
    
    DURATION = (
        (MONTHLY, _('Monthly')),
        (QUARTERLY, _('Quarterly')),
        (BI_ANNUALLY, _('Bi-Annually')),
        (ANNUALLY, _('Annually'))
    )
    
    user = models.ForeignKey(
        to=get_user_model(), 
        on_delete=models.CASCADE
    ) 
    duration = models.CharField(
        choices=DURATION,
        default=MONTHLY,
        max_length=50
    )
    subscription = models.ForeignKey(
        to='dashboard.Subscription',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField( 
        auto_now_add = True, 
        editable = False 
    )
    expire_at = models.DateTimeField( 
        auto_now=False,
        null=True, 
        editable=False
    )

    class Meta:
        db_table = 'subscriptions_log_tbl'
        
class Subscription(models.Model):
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0
    )
    subscription_type = models.CharField(
        max_length=255
    )
    created_at = models.DateTimeField( 
        auto_now_add=True, 
        editable=False 
    )
    updated_at = models.DateTimeField( 
        auto_now=True, 
        editable=True
    )
    
class FriendRequest(models.Model):
    # profile verification fields
    PENDING = 'P'
    ACCEPT = 'A'
    REJECT = 'R'
    
    FRIEND_REQUEST_STATUS = (
        (ACCEPT, _('Accepted')),
        (PENDING, _('Pending')),
        (REJECT, _('Rejected'))
    )
    
    user_requested = models.ForeignKey(
        to=get_user_model(), 
        on_delete=models.CASCADE,
        related_name='users_requested'
    ) 
    user_requesting = models.ForeignKey(
        to=get_user_model(), 
        on_delete=models.CASCADE,
        related_name='users_requesting'
    ) 
    friend_request_status = models.CharField(
        choices=FRIEND_REQUEST_STATUS,
        default=PENDING,
        max_length=50
    )
    created_at = models.DateTimeField( 
        auto_now_add=True, 
        editable=False 
    )
    date_accepted = models.DateTimeField( 
        auto_now=False, 
        null=True,
        editable=True
    )
    
    class Meta:
        db_table = 'friend_request_tbl'
        
class FollowingList(models.Model):
    user_followed = models.ForeignKey(
        to=get_user_model(), 
        related_name='users_followed',
        on_delete=models.CASCADE
    ) 
    user_following = models.ForeignKey(
        to=get_user_model(), 
        on_delete=models.CASCADE,
        related_name='users_following'
    ) 
    created_at = models.DateTimeField( 
        auto_now_add=True, 
        editable=False 
    )
    
    class Meta:
        db_table = 'following_tbl'
        
class Privacy(models.Model):
    pass

class Religion(models.Model):
    pass