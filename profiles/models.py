from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.shortcuts import reverse

class ProfileManager(models.Manager): # extend the manager moel
    def  get_all_profiles(self,me): # function to return all profiles exclude current profile
        profiles = Profile.objects.all().exclude(user = me)
        return profiles
    
    def get_all_profiles_to_invite(self,me) : 
        #function to return all profiles that  i can invite will exclude my self and
        #profiles who are alredy friend with me or i sent invitation to them before
        profiles = Profile.objects.all().exclude(user=me)
        my_profile = Profile.objects.get (user=me) 
        qs = Relationship.objects.filter( Q(sender=my_profile) | Q(receiver= my_profile))
        available = []
        not_available= []
        for relation in qs:
            if relation.status == 'accepted' or relation.status == 'send':
                if relation.sender == my_profile:
                    not_available.append(relation.receiver)
                else:
                    not_available.append(relation.sender)
        for profile in profiles:
            if profile not in not_available:
                available.append(profile)
        return available

class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    bio = models.TextField(max_length=500 , default=" No Bio ...")
    email = models.EmailField(max_length=200 , blank= True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png',upload_to='avatars/')
    #need to install pillow - create media root - select avatar.png
    friends = models.ManyToManyField(User , blank=True, related_name='friends')
    slug = models.SlugField(unique=True , blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField (auto_now_add=True)
    objects = ProfileManager()

    def get_absolute_url(self):
        return reverse('profiles:profile-detail-view', kwargs={"slug" : self.slug})

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_posts_no(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()
    def get_all_authors_posts(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value=='Like':
                total_liked += 1
        return total_liked

    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked        

    def __str__(self):
        return f"{self.user.username} - {self.created.strftime('%d-%m-%y')}" 
# Create your models here.
    # define a function to create a unique slug for each created profile
    # used uuid from utils.py
    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save (self ,*args , **kwargs):
        ex = False
        if self.first_name !=self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="" :
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name)+" " + str(self.last_name))
                ex = Profile.objects.filter(slug = to_slug).exists()
                while ex:
                    to_slug = slugify (to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug = to_slug).exists()
            else:
                to_slug = str(self.user)
            self.slug = to_slug
        super().save(*args , **kwargs)
    

STATUS_CHIOCES = (
    ('send' , 'send'),
    ('accepted' , 'accepted'),
) 

class RelationShipManager(models.Manager):
    def invitations_received(self,receiver): # return profile that send invitation to me (not accepted)
        qs = Relationship.objects.filter(receiver = receiver , status = 'send')
        return qs



class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete= models.CASCADE , related_name='sender')
    receiver = models.ForeignKey (Profile , on_delete= models.CASCADE , related_name= 'receiver')
    status = models.CharField(max_length=10 , choices= STATUS_CHIOCES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField (auto_now_add=True)
    objects = RelationShipManager()

    def __str__(self) -> str:
        return f"{self.sender} - {self.receiver} - {self.status}"
