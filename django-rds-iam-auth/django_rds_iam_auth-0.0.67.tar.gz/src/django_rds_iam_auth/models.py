from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserHasTenant(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    tenant = models.ForeignKey('Tenant', on_delete=models.PROTECT)

    class Meta:
        db_table = 'api_tenant_users'
        auto_created = 'Tenant'


class User(AbstractUser):

    class RoleTypes(models.TextChoices):
        COMMIT_ADMIN = 'Commit Admin', _('Commit Admin')
        TENANT_ADMIN = 'Tenant Admin', _('Tenant Admin')
        ORGANIZATION_ADMIN = 'Organization Admin', _('Organization Admin')
        END_USER = 'End User', _('End User')

    id = models.CharField(max_length=45, unique=True, primary_key=True)
    origin_tenant_id = models.CharField(null=True, blank=False, max_length=255)
    enable_iam = models.BooleanField(null=False, default=False)
    creator_id = models.CharField(null=False, max_length=255,default='system')
    tenants = models.ManyToManyField('Tenant', through='UserHasTenant', blank=True, auto_created=False)
    role = models.ForeignKey(Group, on_delete=models.SET_NULL, default=None, related_name='user_roles', null=True)

    email = models.EmailField(_('email'), blank=True)

    phone_number = models.CharField(_('phone'), null=True, blank=True, max_length=40)

    REQUIRED_FIELDS = ['creator_id', 'id']

    def delete_model(self, using=None, keep_parents=False):
        self.tenants.clear()
        self.is_active = False
        self.enable_iam = False

    @property
    def full_name(self):
        return ' '.join((self.first_name, self.last_name))

    class Meta:
        verbose_name = 'Users management'
        verbose_name_plural = 'Users management'
        abstract = False
        db_table = 'api_user'


class TenantRoles(models.Model):
    tenant = models.ForeignKey('Tenant', on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)

    class Meta:
        db_table = 'api_tenant_roles'


class Tenant(models.Model):

    class StatusTypes(models.TextChoices):
        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')
        INVITED = 'Invited', _('Invited')

    class RegistrationMethods(models.IntegerChoices):
        TEMPORARY = 1
        PREDEFINED = 2

    class SingUpTypes(models.TextChoices):
        ADMIN_SIGN_UP = 'Sign up by admin', _('Sign up by admin')
        SELF_SIGN_UP = 'Self sign up', _('Self sign up')

    id = models.CharField(null=False, max_length=45, primary_key=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=8, choices=StatusTypes.choices, default=StatusTypes.INVITED)
    owner_id = models.CharField(max_length=255, null=False, default='system')
    users = models.ManyToManyField('User', through='UserHasTenant', blank=True)
    parent_tenant = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='child_tenant')
    root_tenant = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True,
                                    related_name='sub_root_tenants')
    address = models.CharField(null=True, blank=True, max_length=255)
    phone_number = models.CharField(null=True, blank=True, max_length=40)
    admin_email = models.EmailField(_("admin's email"), unique=True)
    logo = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_iot_core = models.BooleanField(default=False, verbose_name='IOT core')
    sign_up_type = models.CharField(max_length=16, choices=SingUpTypes.choices, default=SingUpTypes.ADMIN_SIGN_UP)
    registration_method = models.IntegerField(choices=RegistrationMethods.choices, default=RegistrationMethods.TEMPORARY)
    is_fota_required = models.BooleanField(verbose_name='FOTA required', default=False)
    is_organizations_required = models.BooleanField(verbose_name='Organizations management required', default=False)
    roles = models.ManyToManyField(Group, related_name='tenants', through='TenantRoles')

    button_color_1 = models.CharField(null=True, blank=True, max_length=7, verbose_name='Save/submit buttons')
    button_color_2 = models.CharField(null=True, blank=True, max_length=7, verbose_name='Add buttons')
    hover_color = models.CharField(null=True, blank=True, max_length=7, verbose_name='Hover colors')
    org_boxes = models.CharField(null=True, blank=True, max_length=7, verbose_name='Organizations color in tree')
    color_text_1 = models.CharField(null=True, blank=True, max_length=7, verbose_name='Organizations names in tree')

    menu_color = models.CharField(null=True, blank=True, max_length=7, verbose_name='Menu box')
    color_text_2 = models.CharField(null=True, blank=True, max_length=7, verbose_name='Text in menu')

    class Meta:
        verbose_name = 'Accounts management'
        verbose_name_plural = 'Accounts management'
        db_table = 'api_tenant'

    def __str__(self):
        return str(self.id)


class ApplicationRestriction(models.Model):
    version = models.CharField(null=False, blank=False, max_length=255, verbose_name='Deprecate version')
    tenant = models.OneToOneField('Tenant', on_delete=models.PROTECT)

    class Meta:
        db_table = 'api_application_restriction'
        verbose_name_plural = "Versions"

    def __str__(self):
        return f'{self.tenant.name} version'


if not hasattr(Group, 'is_active'):
    field = models.BooleanField(default=True)
    field.contribute_to_class(Group, 'is_active')

if not hasattr(Group, 'is_default'):
    field = models.BooleanField(default=False)
    field.contribute_to_class(Group, 'is_default')

if not hasattr(Group, 'name_alias'):
    field = models.CharField(max_length=255, default=None, null=True)
    field.contribute_to_class(Group, 'name_alias')
