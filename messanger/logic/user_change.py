from messanger.models import Consumer


def change_user_avatar(user, form):
    consumer = Consumer.objects.get(user=user)
    consumer.avatar = form.cleaned_data['avatar']
    consumer.save()