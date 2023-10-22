from django.db import models
import uuid
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from accounts.models import *

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)
    group = models.OneToOneField(to=UserGroup, blank=True, null=True, on_delete=models.CASCADE)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.get_online_count()})"

def get_image_path(instance, filename):
    return join("uploaded_images", instance.user.full_name, filename)

class Attachment(models.Model):
    files = models.FileField(upload_to='uploads/')
    image = models.ImageField(default="default.jpg", upload_to=get_image_path)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    from_user = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages_from_me"
    )
    content = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.from_user.first_name}: {self.content} [{self.created_at}]"

    def last_50_messages():
        return Message.objects.order_by('-created_at').all()[:50]
    
    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        messages = Message.objects.filter(is_seen=False).count()
        data = {'count': messages, 'current_msg': self.content}
        print("Saved!!!!!!!!!!!")
        async_to_sync(channel_layer.send(
            'test_channel_group', {
            'type': 'chat_message',
            'value': json.dumps(data)
            }
        ))
        return super(Message, self).save(*args, **kwargs)
    