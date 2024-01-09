from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('', views.home, name='home'),
    path('room/<str:primary_key>/', views.room, name='room'),
    path('create-room/', views.create_room, name="create-room"),
    path('update-room/<str:primary_key>/', views.update_room, name="update-room"),
    path('delete-room/<str:primary_key>/', views.delete_room, name="delete-room"),
    path('delete-message/<str:primary_key>/', views.delete_message, name='delete-message'),
    path('user-profile/<str:primary_key>/', views.user_profile, name='user-profile'),
    path('update-user/', views.update_user, name='update-user'),
    path('topics/', views.topics_page, name='topics'),
    path('activity/', views.activity_page, name='activity'),
]
