from django.views.generic import View

from messanger.models import Consumer, AddToFriendNotification


class FriendsListMixin(View):
    def dispatch(self, request, *args, **kwargs):
        self.friends = Consumer.objects.get(user=request.user).friends.all()
        return super().dispatch(request, *args, **kwargs)


class NotificationsMixin(View):
    def dispatch(self, request, *args, **kwargs):
        self.notifications = AddToFriendNotification.objects.filter(send_from=request.user)
        self.notif_to_me = AddToFriendNotification.objects.filter(send_to=request.user)
        return super().dispatch(request, *args, **kwargs)
