from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name="index"),
    path("login/",login_user,name="login_user"),
    path("signup/",signup,name="signup_user"),
    path("logout/",logout_user,name="logout"),
    path("addpost/",add_post,name="add_post"),
    path("post/<str:pk>",post_detail,name="post_detail"),
    path("like/<str:pk>",like_post,name="like_post"),
    path("dislike/<str:pk>",dislike_post,name="dislike_post"),
    path("add_comment/<str:pk>",add_comment,name="add_comment"),
    path("del_comment/<int:pk>/<int:id>/",del_comment,name="del_comment"),
    path("profile/",profile,name="profile"),
    path("del_post/<str:id>",del_post,name="del_post"),
    path("<str:anything>",anything,name="anything")
]