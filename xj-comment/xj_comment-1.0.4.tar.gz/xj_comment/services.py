"""
Created on 2022-05-01
@author:刘飞
@description:评论模块逻辑处理
"""
from django.db.models import F
from rest_framework import serializers

from xj_thread.models import ThreadStatistic
from xj_user.models import BaseInfo, DetailInfo
from .models import CommentAbstract


# 从数据库获取评论树
def get_comment_tree(comment, obj, level=1):
    tree = []
    for c in obj:
        user_obj = BaseInfo.objects.filter(id=c.user_id).first()
        user_detail_obj = DetailInfo.objects.filter(user_id=c.user_id).first()
        menu_data = {
            "id": c.id,
            "avatar": user_detail_obj.avatar if user_detail_obj else None,
            "nickname": user_detail_obj.user.nickname if user_detail_obj and user_detail_obj.user else None,
            "is_deleted": c.is_deleted,
            "user_id": c.user_id,
            "full_name": user_obj.full_name if user_obj else None,
            "user_name": user_obj.user_name if user_obj else None,
            "ip": c.ip,
            # "create_time": dateutil.parser.parse(c.create_time).strftime('%Y-%m-%d %H:%M:%S'),
            "create_time": c.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "message": c.message,
            "weight": c.weight,
            "likes": c.likes,
            "favorite": c.favorite,
            "comments": c.comments,
            "shares": c.shares,
            "children": [],
            "level": level
        }
        child = comment.objects.filter(commented_id=c.id, is_deleted=False)
        if child:
            menu_data["children"].append(get_comment_tree(comment, child, level + 1))
            level = 1
        tree.append(menu_data)
    return tree


class CommentServices:
    def __init__(self):
        pass

    @staticmethod
    def comment_list_read(request):
        """评论列表"""
        if request.method == 'GET':
            thread_id = request.query_params.get('thread_id')
            if not thread_id:
                raise serializers.ValidationError('信息id未传。')
            comment = CommentAbstract.get_student_db_model(thread_id=thread_id)
            obj = comment.objects.filter(thread_id=thread_id, commented_id=None, is_deleted=False)
            res = get_comment_tree(comment, obj)
            return res, None

    @staticmethod
    def comment_list_create(request):
        """评论表新增"""
        thread_id = request.data.get('thread_id')
        message = request.data.get('message')
        commented_id = request.data.get('commented_id', None) or None
        if not thread_id:
            raise serializers.ValidationError('信息id未传。')

        # 信息统计表更新数据
        ThreadStatistic.objects.filter(thread_id=thread_id).update(comments=F('comments') + 1)

        # 找到对应评论表
        comment = CommentAbstract.get_student_db_model(thread_id=thread_id)
        # 父评论信息更新
        if commented_id:
            comment.objects.filter(id=commented_id).update(comments=F('comments') + 1)
        # 评论新增
        obj = comment()
        obj.user_id = request.user.get('user_id', None)
        obj.thread_id_id = thread_id
        obj.message = message
        obj.commented_id = commented_id
        obj.save()
        return None, None

    @staticmethod
    def comment_detail(request, pk):
        thread_id = request.data.get('thread_id')
        if not thread_id:
            raise serializers.ValidationError('信息id未传。')
        comment = CommentAbstract.get_student_db_model(thread_id=thread_id)  # 对应的数据表
        comment_obj = comment.objects.filter(id=pk).first()  # 这条评论

        if request.method == 'DELETE':
            if comment_obj:
                # 信息统计表数据更新
                ThreadStatistic.objects.filter(thread_id=thread_id).update(comments=F('comments') - 1)
                # 父评论更新数据
                if comment_obj.commented_id:
                    comment.objects.filter(id=comment_obj.commented_id).update(comments=F('comments') - 1)

                comment_obj.is_deleted = True
                comment_obj.save()
            return None, None
