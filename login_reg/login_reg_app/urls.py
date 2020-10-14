from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
    path('post_message', views.post_message),
    path('post_comment', views.post_comment),
    path('delete_msg/<int:message_id>', views.delete_msg),
    path('delete_cmt/<int:comment_id>', views.delete_cmt),
]