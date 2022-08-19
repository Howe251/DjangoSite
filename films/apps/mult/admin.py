from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import path
from django.http import HttpResponseRedirect
from django.db import models
from django.forms import TextInput, Textarea
from .forms import AdminUrlForm
from .models import Series, Mult, Film, SeriesFilms, Audio, Subs, Genre
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter


admin.site.register(Genre)


class FilmSeriesInline(admin.TabularInline):
    extra = 0
    model = SeriesFilms
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


@admin.register(Film)
class FilmID(admin.ModelAdmin):
    form = AdminUrlForm
    change_list_template = "admin/model_change_list.html"
    change_form_template = "admin/model_change_form.html"
    list_display = ("name", "filmtype", "get_image")
    list_filter = ('isShown', ('seasons', DropdownFilter), ('year', DropdownFilter), ('genre', RelatedDropdownFilter))
    search_fields = ['name', 'description', 'unformated_name', ]
    fieldsets = [
        ("Изменить информацию", {"fields": ['name', 'country', 'seasons', 'filmtype', 'year', 'description', 'genre',
                                            'img', 'img_url', 'unformated_name', 'mult', 'isShown', 'kino_url']})
    ]
    inlines = [FilmSeriesInline,]

    def get_image(self, obj):
        return mark_safe(f'<img src=/media/{obj.img} width="50" height="60">')

    get_image.short_description = "Изображение"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('delete_img/', self.delete_img),
        ]
        return my_urls + urls

    def delete_img(self, request):
        print("Del")
        self.model.objects.all().update(img=None)
        self.message_user(request, "Картинки удалены")
        return HttpResponseRedirect("../")


@admin.register(SeriesFilms)
class SeriesFilmsID(admin.ModelAdmin):
    list_display = ("name", "name_serie", "full_name")
    search_fields = ['name', 'name_serie', ]


class SeriesInline(admin.TabularInline):
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    model = Series


class SubsInline(admin.TabularInline):
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    model = Subs
    fields = ("name", ("name_sub", "autor", "href",))


class AudioInline(admin.TabularInline):
    extra = 0
    model = Audio
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    fields = ("name", ("name_audio", "autor", "href"))


@admin.register(Mult)
class MultID(admin.ModelAdmin):
    form = AdminUrlForm
    change_list_template = "admin/model_change_list.html"
    change_form_template = "admin/model_change_form.html"
    list_display = ("name", "episodes", "get_image")
    list_filter = ('isShown', ('episodes', DropdownFilter), ('genre', RelatedDropdownFilter))
    search_fields = ['name', 'description', ]
    fieldsets = [
        ('Изменить информацию', {'fields': ['name', 'episodes', 'status', 'description', 'img', 'img_url', 'genre', 'unformated_name',
                           'isShown', 'mult', 'kino_url']}),
    ]
    inlines = [SeriesInline, SubsInline, AudioInline]

    def get_image(self, obj):
        return mark_safe(f'<img src=/media/{obj.img} width="50" height="60">')

    get_image.short_description = "Изображение"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('delete_img/', self.delete_img),
        ]
        return my_urls + urls

    def delete_img(self, request):
        self.model.objects.all().update(img=None)
        self.message_user(request, "Картинки удалены")
        return HttpResponseRedirect("../")


@admin.register(Series)
class SeriesID(admin.ModelAdmin):
    list_display = ("name_id", "name", "name_serie", "full_name")
    search_fields = ['name', 'name_serie', "full_name", ]


@admin.register(Subs)
class SubsID(admin.ModelAdmin):
    list_display = ("name", "name_sub", "autor", "href")


@admin.register(Audio)
class AudiosID(admin.ModelAdmin):
    list_display = ("name_audio", "autor", "href", "mult_id")