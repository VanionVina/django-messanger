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
        self.all_notif = 0
        for notif in self.notif_to_me:
            if notif.agreed != False and notif.agreed != True:
                self.all_notif += 1
        for notif in self.notifications:
            if notif.agreed == False or notif.agreed == True:
                self.all_notif += 1
        self.context_notif = {
            'all_notif': self.all_notif,            # All, connected to me
            'notifications': self.notifications,    # From me
            'notif_to_me': self.notif_to_me,        # To me
        }
        return super().dispatch(request, *args, **kwargs)
