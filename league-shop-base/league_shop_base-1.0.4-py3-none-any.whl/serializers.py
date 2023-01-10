
'''Serializers module'''
from rest_framework import serializers

from .models import Champion
from .models import Product
from .models import Skin


class ChampionSerializer(serializers. ModelSerializer):
    class Meta:
        model = Champion
        fields = ['id', 'name', 'roles', 'lanes']


class SkinSerializer(serializers.ModelSerializer):
    '''SkinSerializer class'''
    champion = serializers.CharField(source='champion.name')
    lanes = serializers.CharField(source='champion.lanes')
    roles = serializers.CharField(source='champion.roles')

    class Meta:
        model = Skin
        fields = ['id', 'name', 'champion', 'tier', 'value', 'lanes', 'roles']


class ProductSerializer(serializers.ModelSerializer):
    '''ProductSerializer class'''
    level = serializers.IntegerField(source='discrete_level')
    blue_essence = serializers.IntegerField(source='discrete_blue_essence')
    skins = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    owned_skins = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    permanent_skins = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'level',
            'blue_essence',
            'orange_essence',
            'mythic_essence',
            'region',
            'skins',
            'owned_skins',
            'permanent_skins',
        ]


class ProductUploadSerializer(serializers.ModelSerializer):
    '''ProductUploadSerializer class'''
    skins = serializers.PrimaryKeyRelatedField(many=True, queryset=Skin.objects.all())
    permanent_skins = serializers.PrimaryKeyRelatedField(many=True, queryset=Skin.objects.all())
    owned_skins = serializers.PrimaryKeyRelatedField(many=True, queryset=Skin.objects.all())

    class Meta:
        model = Product
        fields = [
            'username',
            'password',
            'level',
            'blue_essence',
            'orange_essence',
            'mythic_essence',
            'region',
            'skins',
            'permanent_skins',
            'owned_skins',
        ]


class PurchasedProductSerializer(serializers.ModelSerializer):
    '''PurchasedProductSerializer class'''
    level = serializers.IntegerField(source='discrete_level')
    blue_essence = serializers.IntegerField(source='discrete_blue_essence')
    skins = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    owned_skins = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    permanent_skins = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'username',
            'password',
            'level',
            'blue_essence',
            'orange_essence',
            'mythic_essence',
            'region',
            'skins',
            'owned_skins',
            'permanent_skins',
        ]
