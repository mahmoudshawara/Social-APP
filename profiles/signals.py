from django.db.models.signals import post_save , pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile , Relationship
#signal to create a profile when creating a user 
@receiver (post_save ,sender = User)
def post_save_create_profile(sender,instance,created,**kwargs):
    #print('sender',sender)
    #print('instance', instance)
    if created:
        Profile.objects.create(user=instance)
#signal to add friendship when accepting invitation
@receiver(post_save, sender = Relationship)
def post_save_add_to_friends (sender , instance , created , **kwargs):
    relation_sender = instance.sender
    relation_receiver = instance.receiver
    if instance.status == 'accepted':
        relation_sender.friends.add(relation_receiver.user)
        relation_receiver.friends.add(relation_sender.user)
        relation_sender.save()
        relation_receiver.save()        

@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user) 
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()
