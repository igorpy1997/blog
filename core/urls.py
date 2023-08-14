"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog_app/", include("blog_app.urls"))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import include
from blog_app.views import (
    MainPageView,
    RegistrationView,
    CustomPasswordResetView,
    LikePostView,
    GetCommentsView,
    AddCommentView,
    GetPostView,
    PostCreateView,
    PostEditView,
    PostDeleteView,
    AuthorPostsView,
    MyDraftsView,
    DraftPostEditView,
    ContactUsView,
)
from blog_app import views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("main/", MainPageView.as_view(), name="main"),
    path("get_image_filenames/", views.get_image_filenames, name="get_image_filenames"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="main"), name="logout"),
    path("edit_profile/<int:pk>/", views.EditProfileView.as_view(), name="edit_profile"),
    path("custom_reset_password/", CustomPasswordResetView.as_view(), name="custom_reset_password"),
    path("like/<int:post_id>/", LikePostView.as_view(), name="like_post"),
    path("get_comments/<int:post_id>/", GetCommentsView.as_view(), name="get_comments"),
    path("add_comment/<int:post_id>/", AddCommentView.as_view(), name="add_comment"),
    path("get_post/<int:post_id>/", GetPostView.as_view(), name="get_post"),
    path("post_create/", PostCreateView.as_view(), name="create-post"),
    path("edit/<int:pk>/", PostEditView.as_view(), name="edit_post"),
    path("delete/<int:pk>/", PostDeleteView.as_view(), name="delete_post"),
    path("author/<str:author_username>/", AuthorPostsView.as_view(), name="author-posts"),
    path("my-drafts/", MyDraftsView.as_view(), name="my-drafts"),
    path("draft_post/<int:pk>/", DraftPostEditView.as_view(), name="draft_post"),
    path("contact-us/", ContactUsView.as_view(), name="contact-us"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
