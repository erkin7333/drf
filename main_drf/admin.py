from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import (Category, Actyor, Janr, Kino, KinoKadrlar, ReytingYulduzi, Reyting, Review)



class KinoAdmiForm(forms.ModelForm):
    description = forms.CharField(label="Tavsifi", widget=CKEditorUploadingWidget)
    class Meta:
        model = Kino
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ("name", "email")


class MovieShotsInline(admin.TabularInline):
    model = KinoKadrlar
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='100' height='110'")

    get_image.short_description = "Rasm"


@admin.register(Kino)
class KinoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", 'category', 'url', 'draft')
    list_filter = ("category", 'year',)
    search_fields = ('title', 'category__name')
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    actions = ["publish", "unpublish",]
    form = KinoAdmiForm
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (('title', 'tagline',))
        }),
        (None, {
            "fields": ('description',('poster', 'get_image'))
        }),
        (None, {
            "fields": (("year", "world_premiers", "country"))
        }),
        ("Actors", {
            "classes": (('collapse',)),
            "fields": (('actors', 'directors', 'genres', 'category'))
        }),
        (None, {
            "fields": (('budget', 'fees_in_usa', 'fees_in_world', 'fees_in_uz'))
        }),
        ("Options", {
            "fields": (('url', 'draft'))
        })
    )

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='100' height='110'")

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 Yozuvlar yangilandi"
        else:
            message_bit = f"{row_update} Yozuvlar yangilandi"

        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 Yozuvlar yangilandi"
        else:
            message_bit = f"{row_update} Yozuvlar yangilandi"

        self.message_user(request, f"{message_bit}")

    publish.short_description = "Nashr qilish"
    publish.allowed_permission = ["O'zgartirish",]

    unpublish.short_description = "Nashrdan olib tashlash"
    unpublish.allowed_permission = ["O'zgartirish",]

    get_image.short_description = "Plakat"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ("name", "email")


@admin.register(Janr)
class JanrAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(Actyor)
class AktyorAdmin(admin.ModelAdmin):

    list_display = ["name", "age", "get_image"]
    readonly_fields = ["get_image"]

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='50' height='60'")

    get_image.short_discription = "Rasmlar"

@admin.register(Reyting)
class ReytingAdmin(admin.ModelAdmin):

    list_display = ("star", "movie", "ip")


@admin.register(KinoKadrlar)
class KinoKadrlarAdmin(admin.ModelAdmin):

    list_display = ["title", "movie", "get_image"]
    readonly_fields = ["get_image"]

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='50' height='60'")

    get_image.short_discription = "Rasmlar"

admin.site.register(ReytingYulduzi)

admin.site.site_title = "Django Kinosi"
admin.site.site_header = "Django Kinosi"