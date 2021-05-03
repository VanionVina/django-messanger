from channels.db import database_sync_to_async

from django.contrib.auth.models import User

from messanger.models import AddToFriendNotification


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


@database_sync_to_async
def get_notification_data_as_dict(notif_id):
    notification = AddToFriendNotification.objects.get(id=notif_id)
    data = {
        'send_from': notification.send_from.username,
        'send_to': notification.send_to.username,
        'send_from_id': notification.send_from.id,
        'send_from_url': notification.send_from.consumer.get_absolute_url(),
        'id': notif_id
    }
    return data
