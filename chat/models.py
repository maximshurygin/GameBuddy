from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.


class Message(models.Model):
    chat = models.ForeignKey('Chat', null=True, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message in {self.chat} from {self.sender}: {self.content[:20]}"


class Chat(models.Model):
    participants = models.ManyToManyField(get_user_model(), related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        participant_usernames = [
            user.username if user.username else "Удаленный пользователь"
            for user in self.participants.all()
        ]
        return f"Чат #{self.id}"

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def has_unread_messages(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).exists()