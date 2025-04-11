from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Profile(User):
    class Meta:
        proxy = True
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="chat_rooms", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name="chat_rooms", blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Chat Room"
        verbose_name_plural = "Chat Rooms"

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, related_name="messages", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"


# class Reaction(models.Model):
#     REACTION_CHOICES = [
#         ("like", "👍"),
#         ("love", "❤️"),
#         ("laugh", "😂"),
#         ("wow", "😮"),
#         ("sad", "😢"),
#         ("angry", "😠"),
#     ]

#     message = models.ForeignKey(
#         Message, related_name="reactions", on_delete=models.CASCADE
#     )
#     user = models.ForeignKey(User, related_name="reactions", on_delete=models.CASCADE)
#     reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ["message", "user", "reaction_type"]
#         verbose_name = "Reaction"
#         verbose_name_plural = "Reactions"

#     def __str__(self):
#         return f"{self.user.username} reacted with {self.get_reaction_type_display()} to {self.message}"
