from itertools import chain

from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone

from .crypto import encrypt
from .crypto import is_encrypted

SKIN_TIERS = (
    ('ULTIMATE', 'Ultimate'),
    ('MYTHIC', 'Mythic'),
    ('LEGENDARY', 'Legendary'),
    ('EPIC', 'Epic'),
    ('STANDARD', 'Standard'),
    ('BUDGET', 'Budget'),
    ('LIMITED', 'Limited'),
    ('UNKNOWN', 'Unknown'),
)

REGION_CHOICES = [
    ('EUW', 'EUW'),
    ('EUNE', 'EUNE'),
    ('NA', 'NA'),
    ('OC1', 'OCE'),
    ('RU', 'RU'),
    ('TR', 'TR'),
    ('LA1', 'LAN'),
    ('LA2', 'LAS'),
    ('BR', 'BR'),
    ('JP', 'JP'),
]


class Champion(models.Model):
    '''Model representing champion'''
    name = models.CharField(max_length=50)
    roles = models.TextField(blank=True, null=True)
    lanes = models.TextField(blank=True, null=True)

    date_created = models.DateTimeField(default=None, blank=True, null=True)
    date_modified = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        super().save(*args, **kwargs)


class Skin(models.Model):
    '''Model representing champion skin'''
    tier = models.CharField(max_length=9, choices=SKIN_TIERS, default=None)
    name = models.CharField(max_length=50)
    champion = models.ForeignKey(Champion, related_name='skins', on_delete=models.PROTECT)
    value = models.IntegerField(blank=True, null=True, default=None)

    date_created = models.DateTimeField(default=None, blank=True, null=True)
    date_modified = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Skin'
        verbose_name_plural = 'Skins'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        super().save(*args, **kwargs)


class Product(models.Model):
    '''Product model'''

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    region = models.CharField(max_length=4, choices=REGION_CHOICES, default='EUW')
    level = models.FloatField()
    blue_essence = models.PositiveIntegerField()
    orange_essence = models.PositiveIntegerField()
    mythic_essence = models.PositiveIntegerField()
    discrete_level = models.PositiveIntegerField()
    discrete_blue_essence = models.PositiveIntegerField()
    skins = models.ManyToManyField(Skin, blank=True)
    permanent_skins = models.ManyToManyField(
        Skin, blank=True, related_name='permanent_skin_products')
    owned_skins = models.ManyToManyField(Skin, blank=True, related_name='owned_skin_products')
    is_purchased = models.BooleanField(default=False)

    # Fields to optimize fitlering
    all_skins = models.ManyToManyField(Skin, blank=True, related_name='all_skins_products')

    date_created = models.DateTimeField(default=None, blank=True, null=True)
    date_modified = models.DateTimeField(default=None, blank=True, null=True)

    def update_all_skins(self):
        all_skins = chain(self.skins.all(
        ), self.permanent_skins.all(), self.owned_skins.all())
        self.all_skins.set(list(all_skins))

    def __str__(self):
        return f'{self.username}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.date_created = timezone.now()
        if not is_encrypted(self.password):
            self.password = encrypt(self.password)

        self.discrete_blue_essence = (self.blue_essence // 10000) * 10000
        self.discrete_level = (self.level // 10) * 10
        self.date_modified = timezone.now()
        super().save(*args, **kwargs)


@receiver(m2m_changed, sender=Product.skins.through)
@receiver(m2m_changed, sender=Product.permanent_skins.through)
@receiver(m2m_changed, sender=Product.owned_skins.through)
def skins_changed(sender, instance, **kwargs):
    if kwargs['action'] in ['post_add', 'post_remove']:
        instance.update_all_skins()
        instance.save()
