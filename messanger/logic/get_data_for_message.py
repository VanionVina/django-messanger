from channels.db import database_sync_to_async
from django.contrib.auth.models import User
#<!-- 1)from_user.?username?; 2)from_user.absolute_url; 3)from_user.avatar_url; 5)message_time; 6) message.text-->


# @database_sync_to_async
def get_message_data_as_dict(author, text, message_sended):
    author_as_user = User.objects.get(username=author)
    author_username = author_as_user.username
    author_absolute_url = author_as_user.consumer.get_absolute_url()
    author_avatar = author_as_user.consumer.avatar.url
    data = {
        'username': author_username,
        'absolute_url': author_absolute_url,
        'avatar_url': author_avatar,
        'text': text,
        'sended': message_sended,
    }
    return data
