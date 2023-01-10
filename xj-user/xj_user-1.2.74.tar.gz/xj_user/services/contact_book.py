from django.db.models import F
from rest_framework.response import Response

from ..models import ContactBook
from ..utils.custom_response import util_response


class ContactBookService:
    def get_list(self, user_id):
        user_contact_book_list = ContactBook.objects.annotate(user_name=F('friend__user_name'), ).filter(
            user_id=user_id).values("id", "friend_id", "user_name")
        return Response({
            'err': 0,
            'msg': 'OK',
            'data': user_contact_book_list
        })

    def add_friends(self, data):
        friend = ContactBook.objects.filter(user_id=data['user_id'],friend_id=data['friend_id']).first()
        if friend:
            return util_response(data=[], msg='对方已经是你好友')
        user_contact_book = ContactBook.objects.create(**data)
        return Response({
            'err': 0,
            'msg': '添加好友成功',
            'data': {
                "contact_book_id": user_contact_book.id,
                # "token": token,
            }})
