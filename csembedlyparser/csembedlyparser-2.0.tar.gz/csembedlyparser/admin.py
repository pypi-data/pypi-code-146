from django.contrib import admin
from django.conf import settings
from csembedlyparser.models import EmbedlyParsed
from tinymce.widgets import TinyMCE


class EmbedlyParsedAdmin(admin.ModelAdmin):
    list_display = ('id','domain','title','title_original','description','photo_url')
    ordering = ('-id',)
    readonly_fields = ('title_original',)

    fieldsets = (
        ('General',
         {'fields':(('original_url','domain',),)}),
        ('Parsed',
         {'fields':(('parsed','parsed_datetime'),)}),
        ('Data',
         {'fields':(('title','title_original'),'description',('photo_url','thumbnail_url',),('favicon','type',))}),
        ('More',
         {'fields':(('version','url',),('author_name','author_url'),('provider_name','provider_url',),'cache_age',)}),
         
        )   

class TinyMCEEmbedlyParsedAdmin(EmbedlyParsedAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('description', ):
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs=settings.TINYMCE_DEFAULT_CONFIG,
            ))
        return super(TinyMCEEmbedlyParsedAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(EmbedlyParsed, TinyMCEEmbedlyParsedAdmin)
