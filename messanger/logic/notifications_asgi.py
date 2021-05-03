from django.contrib.auth.models import User
from channels.db import database_sync_to_async

from messanger.models import AddToFriendNotification



@database_sync_to_async
def delete_notification(notif_id):
    notif = AddToFriendNotification.objects.get(id=notif_id)
    notif.delete()

@database_sync_to_async
def update_notification_answer(notif_id, answer):
    notif = AddToFriendNotification.objects.get(id=notif_id)
    notif.agreed = answer
    notif.save()
    return notif.send_from.id


@database_sync_to_async
def create_new_notification(from_user, to_user):
    send_from_user = User.objects.get(id=int(from_user))
    send_to_user = User.objects.get(id=int(to_user))
    new_notif = AddToFriendNotification.objects.create(send_from=send_from_user, send_to=send_to_user)
    # new_notif = AddToFriendNotification(send_from=send_from_user, send_to=send_to_user)
    return new_notif 


@database_sync_to_async
def friends_notif_true(notif_id):
    notif = AddToFriendNotification.objects.get(id=int(notif_id))
    notif.send_from.consumer.friends.add(notif.send_to.consumer)
    notif.send_to.consumer.friends.add(notif.send_from.consumer)