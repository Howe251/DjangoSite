from . import views
from django.urls import include, path

app_name = 'mult'
urlpatterns = [
    path('', views.mainpage, name='glavnaya'),
    path('mults/', views.mult_list, name='mult'),
    path("search/", views.search, name='search'),
    path("mults/<int:mult_id>/", views.DetailedView, name='detail'),
    path("films/", views.film_list, name='film'),
    path("films/<int:film_id>/", views.film_detail, name='detailfilm'),
]
