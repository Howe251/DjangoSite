from . import views
from django.urls import include, path
# from .views import LoginView

app_name = 'mult'
urlpatterns = [
    path('admin/login', views.LoginView.as_view(), name='login'),
    path('', views.mainpage, name='glavnaya'),
    path('mults/', views.mult_list, name='mult'),
    path("search/", views.search, name='search'),
    path("mults/<int:mult_id>/", views.DetailedView, name='detail'),
    path("films/", views.film_list, name='film'),
    path("films/<int:film_id>/", views.film_detail, name='detailfilm'),
    path("login/", views.LoginView.as_view(), name='login'),
    path("cabinet/", views.CabinetView.as_view(), name='cabinet'),
    path("logout/", views.out, name='logout'),
    path("register/", views.create_user, name='register'),
    path('mults/<int:pk>/like/', views.AddLike.as_view(), name='like'),
    path('films/<int:pk>/like/', views.AddLike.as_view(), name='flike'),
    path('mults/<int:pk>/dislike/', views.AddDislike.as_view(), name='dislike'),
    path('films/<int:pk>/dislike/', views.AddDislike.as_view(), name='fdislike'),
    # path('accounts/', include('django.contrib.auth.urls')),
]

# from django.contrib.auth import views
#
# urlpatterns += [path('login/', views.LoginView.as_view(
#             template_name="registration/login.html",
#             authentication_form=UserLoginForm
#             ),
#         name='login')]