from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.webproj, name="webproj"),
    path('add/', views.create_post, name='create_post'),
    path('edit_post/', views.edit_post, name='edit_post'),
    path('news/', views.news_view, name='news_view'),
    path('detail_post/<int:id>/', views.detail_post, name='detail_post'),
    path('delete_post/', views.delete_post, name='delete_post'),
    path('register/', views.register_view, name="register"),
    path('update-profile/', views.update_profile_view, name="update_profile_view"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

