from django.db import models
from django.utils import timezone


# Create your models here.


# class Permission(models.Model):
#     """ 9、User_Permission  权限组表 [1-N] """
#     permission_id = models.IntegerField(verbose_name='权限ID', primary_key=True, help_text='必填。不自动生成，由运营人员统一设置。')
#     permission_name = models.CharField(verbose_name='权限名称', max_length=255, blank=True, null=True, help_text='权限名称')
#
#     class Meta:
#         db_table = 'user_permission'
#         verbose_name_plural = "09. 用户 - 权限组表"
#
#     def __str__(self):
#         # return f"{self.user_name}({self.full_name})"
#         return f"{self.permission_name}"


# class PermissionValue(models.Model):
#     """
#     10、User_Permission_Value 权限组值表 [1-N]
#     权限标识值，一个permission_id可以对应多个value，多值形成一组权限。值为宏名，需要多语言翻译
#     """
#     permission = models.ForeignKey(Permission, verbose_name='权限ID', on_delete=models.DO_NOTHING, help_text='')
#     module = models.CharField(verbose_name='模型名称', max_length=255, blank=True, null=True, help_text='')
#     feature = models.CharField(verbose_name='功能专注点', max_length=255, blank=True, null=True,
#                                help_text='group: 按用户组给权限, route: 按路由给权限, point: 按交互点给权限, ..., category: 类别权限')
#     permission_value = models.CharField(verbose_name='权限标识值', max_length=255, blank=True, null=True,
#                                         help_text='权限标识值，一个permission_id可以对应多个value，多值形成一组权限。值为宏名，需要多语言翻译')
#     type = models.CharField(verbose_name='类型', max_length=255, blank=True, null=True, help_text='暂不使用')
#     relate_value = models.CharField(verbose_name='权限内容关联值', max_length=255, blank=True, null=True, help_text='')
#     config = models.JSONField(verbose_name='权限更多配置', max_length=255, blank=True, null=True, help_text='权限更多配置，常用于前端路由')
#     is_enable = models.CharField(verbose_name='是否启用权限', max_length=1, blank=True, null=True, help_text='')
#     is_system = models.CharField(verbose_name='是否系统权限', max_length=1, blank=True, null=True,
#                                  help_text='是否系统权限，系统权限不可以删除，默认SUPER_ADMINISTRATOR的所有value都是系统权限。')
#     is_ban = models.CharField(verbose_name='是否禁用', max_length=1, blank=True, null=True,
#                               help_text='是否全部禁用该权限，Y禁用，N允许，默认N。使用减法原则，约定无权限值则视为允许。')
#     ban_view = models.CharField(verbose_name='是否可看', max_length=1, blank=True, null=True, help_text='')
#     ban_edit = models.CharField(verbose_name='是否编辑', max_length=1, blank=True, null=True, help_text='')
#     ban_add = models.CharField(verbose_name='是否插入', max_length=1, blank=True, null=True, help_text='')
#     ban_delete = models.CharField(verbose_name='是否删除', max_length=1, blank=True, null=True, help_text='')
#     description = models.CharField(verbose_name='权限值', max_length=1, blank=True, null=True, help_text='')
#     permission_code = models.BooleanField(verbose_name='是否系统权限', blank=True, null=True, help_text='')
#
#     class Meta:
#         db_table = 'user_permission_value'
#         verbose_name_plural = "10. 用户 - 权限组值表"
#
#     def __str__(self):
#         # return f"{self.user_name}({self.full_name})"
#         return f"{self.permission_value}"


# class Group(models.Model):
#     """ 11、User_Group 分组表 """
#     id = models.AutoField(verbose_name='ID', primary_key=True)
#     group = models.CharField(verbose_name='用户组', max_length=32, blank=True, null=True, help_text='')
#     parent_group = models.CharField(verbose_name='父组', max_length=32, blank=True, null=True, help_text='')
#     permission = models.ForeignKey(Permission, verbose_name='权限ID', on_delete=models.DO_NOTHING, blank=True, null=True,
#                                    help_text='')
#     description = models.CharField(verbose_name='描述', max_length=32, blank=True, null=True, help_text='')
#
#     class Meta:
#         db_table = 'user_group'
#         verbose_name_plural = "11. 用户 - 分组表"
#
#     def __str__(self):
#         return f"{self.description}"


class BaseInfo(models.Model):
    """ 1、User_Base_Info 基础信息表 [NF1] """
    # platform_uid = models.BigIntegerField(verbose_name='平台用户ID', db_index=True)
    # platform = models.ForeignKey(Platform, on_delete=models.DO_NOTHING, verbose_name='平台ID',)
    id = models.AutoField(verbose_name='ID', primary_key=True)
    user_name = models.CharField(verbose_name='用户名', max_length=128, unique=True, blank=True, null=True, db_index=True,
                                 help_text='登录的用户名')
    full_name = models.CharField(verbose_name='姓名', max_length=128, blank=True, null=True, db_index=True,
                                 help_text='用户的真实姓名（未实名验证）')
    nickname = models.CharField(verbose_name='昵称', max_length=128, blank=True, null=True, help_text='')
    phone = models.CharField(verbose_name='手机', max_length=128, unique=True, blank=True, null=True, db_index=True,
                             help_text='登录用的手机号')
    email = models.EmailField(verbose_name='邮箱', unique=True, blank=True, null=True, db_index=True, help_text='登录用的邮箱')
    wechat_openid = models.CharField(verbose_name='微信开放号', max_length=128, unique=True, blank=True, null=True,
                                     db_index=True, help_text='微信用户开放ID，注意openid是微信的专用名词')
    user_info = models.JSONField(verbose_name='用户信息', blank=True, null=True, help_text='用户扩展信息')
    # user_group = models.ForeignKey(Group, verbose_name='用户分组', blank=True, null=True, on_delete=models.DO_NOTHING, help_text='')
    # permission = models.ForeignKey(Permission, verbose_name='用户权限', blank=True, null=True, on_delete=models.DO_NOTHING, help_text='')
    register_time = models.DateTimeField(verbose_name='注册时间', default=timezone.now, help_text='')

    class Meta:
        db_table = 'user_base_info'
        # unique_together = [['platform', 'platform_uid'], ['platform', 'user_name']]
        verbose_name_plural = "01. 用户 - 基础信息"

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.user_name}"

    def get_group_desc(self):
        return self.user_group.description if self.user_group else ""

    def get_permission_desc(self):
        return self.permission.permission_name if self.permission else ""


class Auth(models.Model):
    """ 2、User_Auth 安全认证表 [1-1] """
    user = models.ForeignKey(BaseInfo, verbose_name='用户', unique=False, on_delete=models.DO_NOTHING, help_text='登录的用户名')
    password = models.CharField(verbose_name='密码', max_length=255, blank=True, null=True, help_text='登录的密码')
    plaintext = models.CharField(verbose_name='PT', max_length=255, blank=True, null=True, help_text='')
    salt = models.CharField(verbose_name='盐', max_length=32, blank=True, null=True, help_text='加密盐由六位数字和字母组成，区分大小写')
    algorithm = models.CharField(verbose_name='加密算法', max_length=255, blank=True, null=True,
                                 help_text='系统同时支持多种加密算法，旧版为MD5，新版为SHA1')
    token = models.CharField(verbose_name='临时令牌', max_length=255, blank=True, null=True, help_text='用户令牌，用于验证用户有效期')
    ticket = models.CharField(verbose_name='临时票据', max_length=255, blank=True, null=True, help_text='用户提供第三方单点登录的票据')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, help_text='')
    # last_update_ip = models.CharField(verbose_name='最后登录网络地址',  max_length=32, blank=True, null=True, help_text='')
    update_time = models.DateTimeField(verbose_name='最后登录时间', auto_now=True, blank=True, null=True, help_text='')

    class Meta:
        db_table = 'user_auth'
        verbose_name_plural = "02. 用户 - 安全认证"

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.user.user_name}"


class DetailInfo(models.Model):
    """ 3、User_Detail_Info 详细信息表 [1-1] """
    user = models.OneToOneField(BaseInfo, verbose_name='用户', unique=True, on_delete=models.DO_NOTHING,
                                help_text='登录用的用户名')
    real_name = models.CharField(verbose_name='真实姓名', max_length=255, blank=True, null=True, db_index=True,
                                 help_text='实名认证后的真名')
    sex = models.CharField(verbose_name='性别', max_length=1, blank=True, null=True, help_text='0未知 1男 2女')
    birth = models.DateField(verbose_name='生日', blank=True, null=True, help_text='')
    tags = models.CharField(verbose_name='个人标签', max_length=255, blank=True, null=True, help_text='多个标签以英文;号为分隔符')
    signature = models.CharField(verbose_name='个性签名', max_length=255, blank=True, null=True, help_text='')
    avatar = models.CharField(verbose_name='个人头像', max_length=255, blank=True, null=True, help_text='')
    cover = models.CharField(verbose_name='个人封面', max_length=255, blank=True, null=True, help_text='')
    language = models.CharField(verbose_name='语言', max_length=32, blank=True, null=True, help_text='')
    region_code = models.BigIntegerField(verbose_name='行政区划编码', blank=True, null=True, db_index=True, help_text='')
    more = models.JSONField(verbose_name='更多信息', max_length=255, blank=True, null=True,
                            help_text='更多信息用来存放用户可能填写的扩展内容，由于很多信息不是必填或必须存在的，因此不单独建字段。')
    field_1 = models.CharField(verbose_name='字段1', max_length=255, blank=True, null=True, help_text='')
    field_2 = models.CharField(verbose_name='字段2', max_length=255, blank=True, null=True, help_text='')
    field_3 = models.CharField(verbose_name='字段3', max_length=255, blank=True, null=True, help_text='')
    field_4 = models.CharField(verbose_name='字段4', max_length=255, blank=True, null=True, help_text='')
    field_5 = models.CharField(verbose_name='字段5', max_length=255, blank=True, null=True, help_text='')
    field_6 = models.CharField(verbose_name='字段6', max_length=255, blank=True, null=True, help_text='')
    field_7 = models.CharField(verbose_name='字段7', max_length=255, blank=True, null=True, help_text='')
    field_8 = models.CharField(verbose_name='字段8', max_length=255, blank=True, null=True, help_text='')
    field_9 = models.CharField(verbose_name='字段9', max_length=255, blank=True, null=True, help_text='')
    field_10 = models.CharField(verbose_name='字段10', max_length=255, blank=True, null=True, help_text='')
    field_11 = models.CharField(verbose_name='字段11', max_length=255, blank=True, null=True, help_text='')
    field_12 = models.CharField(verbose_name='字段12', max_length=255, blank=True, null=True, help_text='')
    field_13 = models.CharField(verbose_name='字段13', max_length=255, blank=True, null=True, help_text='')
    field_14 = models.CharField(verbose_name='字段14', max_length=255, blank=True, null=True, help_text='')
    field_15 = models.CharField(verbose_name='字段15', max_length=255, blank=True, null=True, help_text='')

    class Meta:
        db_table = 'user_detail_info'
        verbose_name_plural = "03. 用户 - 详细信息"

    def __str__(self):
        # return f"{self.user_name}({self.real_name})"
        return f"{self.user.user_name}"


# 扩展字段的下拉选项
type_choices = (
    ('image', '图片-image'),
    ('text', '输入框-text'),
    ('plain', '禁止编辑-plain'),
    ('number', '数字类型-number'),
    ('time', ' 时间类型-time'),
    ('select', '选择框-select'),
    ('upload', '上传类型-upload'),
    ('textarea', '文本域-textarea'),
    ('password', '密码-password'),
    ('switch', '开关-switch'),
    ('radio', '视频-radio'),
    ('checkBox', '多选-checkBox'),
    ('date', '日期-date'),
    ('month', '月份-month'),
    ('year', '年-year'),
    ('cascader', '多选-cascader'),
    ('slot', '插槽-slot'),
    ('editor', '富文本-editor')
)


class ExtendField(models.Model):
    """ 4、User_Extend_Field 扩展字段表 [1-1] """
    field = models.CharField(verbose_name='自定义字段', max_length=255, unique=True, blank=True, null=True, db_index=True, help_text='当已有字段不能满足的时候的扩展字段')
    field_index = models.CharField(verbose_name='映射索引名', max_length=255, unique=True, blank=True, null=True, help_text='映射到扩展数据表的字段名，如：field_x')
    description = models.CharField(verbose_name='字段描述', max_length=255, blank=True, null=True, help_text='')
    type = models.CharField(verbose_name='类型', max_length=255, blank=True, null=True, help_text='', choices=type_choices)
    config = models.JSONField(verbose_name='配置', blank=True, null=True, help_text='')
    default = models.CharField(verbose_name='默认值', max_length=255, blank=True, null=True, help_text='')
    sort = models.IntegerField(verbose_name='排序', blank=True, null=True, help_text='')

    class Meta:
        db_table = 'user_extend_field'
        verbose_name_plural = "04. 用户 - 扩展字段"

    def __str__(self):
        return f"{self.field}"


class AccessLog(models.Model):
    """ 5、*User_Access_Log 访问日志表 [1-N] """
    user = models.ForeignKey(BaseInfo, verbose_name='用户', on_delete=models.DO_NOTHING, help_text='用户ID')
    ip = models.CharField(verbose_name='IP', max_length=128, blank=True, null=True, help_text='登录的IP地址')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, help_text='')
    client_info = models.JSONField(verbose_name='客户端信息', blank=True, null=True, help_text='')
    more = models.JSONField(verbose_name='更多信息', max_length=255, blank=True, null=True, help_text='留用')

    class Meta:
        db_table = 'user_access_log'
        verbose_name_plural = "05. 用户 - 访问日志表"

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.user.user_name}"


class History(models.Model):
    """ 6、*User_History 操作历史表 [1-N] """
    user = models.ForeignKey(BaseInfo, verbose_name='用户', on_delete=models.DO_NOTHING, help_text='用户ID')
    field = models.CharField(verbose_name='操作字段', max_length=32, blank=True, null=True, help_text='被用户修改的字段')
    old_value = models.CharField(verbose_name='旧值', max_length=255, blank=True, null=True, help_text='修改前的值')
    new_value = models.CharField(verbose_name='新值', max_length=255, blank=True, null=True, help_text='修改后的值')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, help_text='')

    class Meta:
        db_table = 'user_history'
        verbose_name_plural = "06. 用户 - 操作历史表"

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.user.user_name}"


class RestrictRegion(models.Model):
    """ 7、*User_Restrict_Region 限制范围表"""
    user = models.ForeignKey(BaseInfo, verbose_name='用户', on_delete=models.DO_NOTHING, help_text='用户ID')
    region_code = models.BigIntegerField(verbose_name='允许的行政区划编码', blank=True, null=True, db_index=True,
                                         help_text='在国内参考 GB/T2260-2002中国行政区划代码，有6位数 9位数 12位数，非中国地区以9开头')

    class Meta:
        db_table = 'user_restrict_region'
        verbose_name_plural = "07. 用户 - 限制范围表"

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.user.user_name}"


class Platform(models.Model):
    """ 8、*User_Platform 平台表 """
    platform_id = models.IntegerField(verbose_name='平台ID', primary_key=True, help_text='必填。不自动生成，由运营人员统一设置。')
    platform_name = models.CharField(verbose_name='平台名称', max_length=128, help_text='必填。平台名称可以是中文、英文、俄文等。')
    platforms_to_users = models.ManyToManyField(BaseInfo, through='PlatformsToUsers', help_text='平台用户多对多')

    class Meta:
        db_table = 'user_platform'
        verbose_name_plural = "07. 用户 - 平台表"

    def __str__(self):
        return f"{self.platform_name}"

    # 以上代码执行的Sql语句
    # CREATE TABLE `user_platform`(`platform_id` integer NOT NULL PRIMARY KEY, `platform_name` varchar(128) NOT NULL);


class PlatformsToUsers(models.Model):
    """ 9、*User_Platforms_To_Users - 多对多平台记录表 [N-N] """
    user = models.ForeignKey(BaseInfo, verbose_name='用户', on_delete=models.DO_NOTHING, db_column='user_id',
                             help_text='')
    platform = models.ForeignKey(Platform, verbose_name='平台', on_delete=models.DO_NOTHING, help_text='')
    platform_user_id = models.BigIntegerField(verbose_name='平台用户ID', blank=True, null=True, db_index=True, help_text='')

    class Meta:
        db_table = 'user_platforms_to_users'
        verbose_name_plural = "09. 用户 - 多对多平台记录表"
        managed = False

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.user.user_name}"


class ContactBook(models.Model):
    """ 10、*user_contact_book - 用户联系簿表 [1-N] """
    user = models.ForeignKey(BaseInfo, verbose_name='用户', related_name="user_set", on_delete=models.DO_NOTHING,
                             help_text='')
    # user_id = models.IntegerField(verbose_name='用户', help_text='')
    friend = models.ForeignKey(BaseInfo, verbose_name='朋友', related_name="friend_set", on_delete=models.DO_NOTHING,
                               help_text='待删')
    phone = models.JSONField(verbose_name='手机号', blank=True, null=True, help_text='')
    phones = models.JSONField(verbose_name='多个手机号', blank=True, null=True, help_text='')
    telephone = models.JSONField(verbose_name='电话号码', blank=True, null=True, help_text='')
    telephones = models.JSONField(verbose_name='多个电话号码', blank=True, null=True, help_text='')
    email = models.EmailField(verbose_name='邮箱', unique=True, blank=True, null=True, db_index=True, help_text='邮箱')
    qq = models.CharField(verbose_name='QQ', max_length=255, blank=True, null=True, help_text='')
    address = models.CharField(verbose_name='地址', max_length=255, blank=True, null=True, help_text='')
    more = models.JSONField(verbose_name='更多', blank=True, null=True, help_text='')
    remarks = models.CharField(verbose_name='标记', max_length=255, blank=True, null=True, help_text='')

    class Meta:
        db_table = 'user_contact_book'
        verbose_name_plural = "10. 用户 - 联系簿表"

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.user_name}"


class UserSsoServe(models.Model):
    """ 11、User_Sso_Serve - 用户单点登录服务表 [NF1] """
    sso_code = models.CharField(verbose_name='单点登录代码', max_length=255, blank=True, null=True, help_text='')
    sso_name = models.CharField(verbose_name='单点登录名', max_length=255, blank=True, null=True, help_text='')
    sso_url = models.CharField(verbose_name='单点登录地址', max_length=255, blank=True, null=True, help_text='')
    description = models.CharField(verbose_name='描述', max_length=255, blank=True, null=True, help_text='')

    class Meta:
        db_table = 'user_sso_serve'
        verbose_name_plural = "11. 用户 - 单点登录服务表"

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.sso_code}"


class UserSsoToUser(models.Model):
    """ 12、User_Sso_To_User - 多对多单点登录记录表 [NF1] """
    sso_serve = models.ForeignKey(UserSsoServe, verbose_name='单点登录服务ID', on_delete=models.DO_NOTHING,
                                  help_text='')
    user = models.ForeignKey(BaseInfo, verbose_name='用户', on_delete=models.DO_NOTHING, help_text='')
    sso_unicode = models.CharField(verbose_name='单点登录地址', max_length=255, blank=True, null=True, help_text='')
    sso_ticket = models.CharField(verbose_name='描述', max_length=255, blank=True, null=True, help_text='')
    app_id = models.CharField(verbose_name='服务授权app', max_length=255, blank=True, null=True, help_text='')

    class Meta:
        db_table = 'user_sso_to_user'
        verbose_name_plural = "12. 用户 - 多对多单点登录记录表"

    def __str__(self):
        return f"{self.sso_unicode}"


class UserRelateType(models.Model):
    """ 13、User_Relate_Type - 用户关系类型表 """
    id = models.AutoField(verbose_name='ID', primary_key=True)
    relate_key = models.CharField(verbose_name='关系搜索key', max_length=50, blank=True, null=True, default="", help_text='')
    relate_name = models.CharField(verbose_name='关系搜索名称', max_length=50, blank=True, null=True, default="", help_text='')
    description = models.CharField(verbose_name='关系描述', max_length=255, blank=True, null=True, default="", help_text='')

    class Meta:
        db_table = 'user_relate_type'
        verbose_name_plural = "13. 用户 - 关系类型表"

    def __str__(self):
        return f"{self.relate_key}"


class UserRelateToUser(models.Model):
    """ 14、User_Relate_To_User - 多对多关系类型表 """
    id = models.AutoField(verbose_name='ID', primary_key=True)
    user = models.ForeignKey(to="BaseInfo", verbose_name='关系搜索key', related_name="relate_user_id_alias", blank=True, null=True, help_text='', on_delete=models.DO_NOTHING)
    with_user = models.ForeignKey(to="BaseInfo", verbose_name='关系搜索名称', related_name="relate_with_user_id_alias", blank=True, null=True, help_text='', on_delete=models.DO_NOTHING)
    user_relate_type = models.ForeignKey(to=UserRelateType, verbose_name='关系描述', blank=True, null=True, help_text='', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'user_relate_to_user'
        verbose_name_plural = "14. 用户 - 多对多关系类型表"

    def __str__(self):
        return f"{self.id}-{self.with_user_id}"
