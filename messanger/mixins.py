from django.views.generic import View

from messanger.models import Consumer


class FriendsListMixin(View):
    def dispatch(self, request, *args, **kwargs):
        self.friends = Consumer.objects.get(user=request.user).friends.all()
        return super().dispatch(request, *args, **kwargs)


