from django.db import models
import socket
# from apps.user.models import User
from xj_thread.models import Thread

SHARD_TABLE_NUM = 10


# class CommentAllow(models.Model):
#     class Meta:
#         db_table = 'comment_comment_allow'
#         verbose_name_plural = '评论许可表'
#     id = models.BigAutoField(verbose_name='ID', primary_key=True)
#     thread_id = models.ForeignKey(verbose_name='信息ID', to=Thread, db_column='thread_id', related_name='+',
#                                   on_delete=models.DO_NOTHING)
#     user_id = models.ForeignKey(verbose_name='用户ID', to=User, db_column='user_id', related_name='+',
#                                 on_delete=models.DO_NOTHING)


class CommentAbstract(models.Model):
    class Meta:
        ordering = ['-create_time']
        abstract = True

    id = models.BigAutoField(verbose_name='评论ID', primary_key=True)
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False)

    thread_id = models.ForeignKey(verbose_name='信息ID', to=Thread, db_column='thread_id', related_name='+',
                                  on_delete=models.DO_NOTHING)
    user_id = models.BigIntegerField(verbose_name='用户ID', db_index=True)

    ip = models.GenericIPAddressField(verbose_name='IP地址', protocol='both',
                                      default=socket.gethostbyname(socket.gethostname()))
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)  # 不显示，系统自动填。

    message = models.TextField(verbose_name='评论内容')
    commented_id = models.BigIntegerField(verbose_name='被评论ID', null=True, blank=True)

    weight = models.FloatField(verbose_name='权重', default=0, db_index=True)
    likes = models.IntegerField(verbose_name='点赞数', default=0)
    favorite = models.IntegerField(verbose_name='收藏数', default=0)
    comments = models.IntegerField(verbose_name='评论数', default=0)
    shares = models.IntegerField(verbose_name='分享数', default=0)
    _category_model_dict = {}  # help to reuse the model object

    def __str__(self):
        return f"{self.id}"

    @classmethod
    def get_student_db_model(cls, thread_id=None):  # 分表
        suffix = int(thread_id) % SHARD_TABLE_NUM  # 分表的数量【通过取余决定】
        if suffix == 0:
            table_name = 'comment_comment'
        else:
            table_name = f'comment_comment_{suffix}'

        # 构造一个私有字段_user_model_dict来存储模型，
        # 它可以帮助加快获取模型的速度
        if table_name in cls._category_model_dict:
            return cls._category_model_dict[table_name]

        class Meta:
            db_table = table_name

        attrs = {
            '__module__': cls.__module__,
            'Meta': Meta
        }
        # 第一个参数是对象名
        # 第二:类
        # 类字段信息
        user_db_model = type(f'comment_comment_{suffix}', (cls,), attrs)
        cls._category_model_dict[table_name] = user_db_model
        return user_db_model

    # 根据category_id来区分存在哪个表中
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        suffix = int(self.thread_id_id) % SHARD_TABLE_NUM
        if suffix == 0:
            db_name = 'comment_comment'
        else:
            db_name = f'comment_comment_{suffix}'
        self._meta.db_table = db_name
        super(CommentAbstract, self).save(force_insert, force_update, using, update_fields)


class Comment(CommentAbstract):
    class Meta:
        db_table = 'comment_comment'
        verbose_name = '评论表'
        verbose_name_plural = verbose_name


class Comment1(CommentAbstract):
    class Meta:
        db_table = 'comment_comment_1'
        verbose_name = '评论表1'
        verbose_name_plural = verbose_name


class Comment2(CommentAbstract):
    class Meta:
        db_table = 'comment_comment_2'
        verbose_name = '评论表2'
        verbose_name_plural = verbose_name


class Comment3(CommentAbstract):
    class Meta:
        db_table = 'comment_comment_3'
        verbose_name = '评论表3'
        verbose_name_plural = verbose_name


class Comment4(CommentAbstract):
    class Meta:
        db_table = 'comment_comment_4'
        verbose_name = '评论表4'
        verbose_name_plural = verbose_name


class Comment5(CommentAbstract):
    class Meta:
        db_table = 'comment_comment_5'
        verbose_name = '评论表5'
        verbose_name_plural = verbose_name


class Comment6(CommentAbstract):
    class Meta:
        db_table = 'comment_comment_6'
        verbose_name = '评论表6'
        verbose_name_plural = verbose_name


class Comment7(CommentAbstract):
    class Meta:
        db_table = 'comment_comment_7'
        verbose_name = '评论表7'
        verbose_name_plural = verbose_name


class Comment8(CommentAbstract):
    class Meta:
        db_table = 'comment_comment_8'
        verbose_name = '评论表8'
        verbose_name_plural = verbose_name


class Comment9(CommentAbstract):
    class Meta:
        db_table = 'comment_comment_9'
        verbose_name = '评论表9'
        verbose_name_plural = verbose_name
