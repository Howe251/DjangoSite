from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import path
from django.http import HttpResponseRedirect
from .models import Series, Mult, Film, SeriesFilms, Audio

#admin.site.register(Mult)
admin.site.register(Series)
admin.site.register(SeriesFilms)
admin.site.register(Audio)

@admin.register(Film)
class FilmID(admin.ModelAdmin):
    change_list_template = "admin/model_change_list.html"
    list_display = ("name", "filmtype", "get_image")
    list_filter = ('isShown',)

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


@admin.register(Mult)
class MultID(admin.ModelAdmin):
    change_list_template = "admin/model_change_list.html"
    list_display = ("name", "episodes", "get_image")
    list_filter = ('isShown',)

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
