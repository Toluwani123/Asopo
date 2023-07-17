from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.core.exceptions import PermissionDenied


INTERESTS = (
    ("FRONTEND", "Frontend Dev."),
    ("BACKEND", "Backend Dev."),
    ("FULLSTACK", "FullStack Dev."),
    ("BLOCKCHAIN", "Blockchain Dev."),
    ("DATA_ANALYSIS", "Data Analyst"),
)

CUSTOM = (
    ("CUSTOMIZE", "Custom"),
    ("NO_CUSTOM", "No Custom"),
   
)


class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="creator-pictures/")
    contact_email = models.EmailField()
    profession_1 = models.CharField(
        max_length=15, choices=INTERESTS, null=True, blank=True
    )
    profession_2 = models.CharField(
        max_length=15, choices=INTERESTS, null=True, blank=True
    )
    profession_3 = models.CharField(
        max_length=15, choices=INTERESTS, null=True, blank=True
    )
    contact_phone = models.CharField(max_length=20)
    website = models.URLField()
    

    def __str__(self):
        return self.user.email


class EndUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    required_1 = models.CharField(
        max_length=15, choices=INTERESTS, null=True, blank=True
    )
    required_2 = models.CharField(
        max_length=15, choices=INTERESTS, null=True, blank=True
    )
    required_3 = models.CharField(
        max_length=15, choices=INTERESTS, null=True, blank=True
    )

    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="enduserpictures/")

    def __str__(self):
        return self.user.email


class Post(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to="creator-pictures/")
    closed = models.BooleanField(default=False)
    payed = models.BooleanField(default= False)
    field = models.CharField(
        max_length=15, choices=INTERESTS, null=True, blank=True
    )
    demo_picture_1 = models.ImageField(null=True, blank=True, upload_to="projectpictures/")
    demo_picture_2 = models.ImageField(null=True, blank=True, upload_to="projectpictures/")
    demo_picture_3 = models.ImageField(null=True, blank=True, upload_to="projectpictures/")

    def __str__(self):
        return f"{self.creator.user.email} - {self.title}"

    def save(self, *args, **kwargs):
 
        if not isinstance(self.creator, Creator):
            raise PermissionDenied("Only creators can access this model.")
        super().save(*args, **kwargs)


class Message(models.Model):
    
    author = models.ForeignKey(User, related_name='end_user_chat', on_delete=models.CASCADE)
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.author.user.email
    
    def last_10():
        return Message.objects.order_by('-time_stamp').all()[:10]
    

class Bid(models.Model):
    project = models.ForeignKey(Post, related_name='bids', on_delete=models.CASCADE)
    bidder = models.ForeignKey(EndUser, on_delete=models.DO_NOTHING)
    bid_price = models.PositiveIntegerField()
    custom_option = models.CharField(
        max_length=15, choices=CUSTOM, null=False, blank=False
    )
    comments = models.TextField(default="None")
    accepted = models.BooleanField(default=False)
    payed = models.BooleanField(default= False)

    def __str__(self):
        return self.project.title
    def highest_bids():
        return Bid.objects.order_by('bid_price').all()[:10]