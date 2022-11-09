"""merchex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import litreviewapp.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", litreviewapp.views.login_page, name="login"),
    path("logout/", litreviewapp.views.logout_user, name="logout"),
    path("feed/", litreviewapp.views.feed, name="feed"),
    path("signup/", litreviewapp.views.signup_page, name="signup"),
    path("create_ticket/", litreviewapp.views.create_ticket, name="createticket"),
    path("create_review/", litreviewapp.views.create_review, name="createreview"),
    path("subscribe/", litreviewapp.views.follow_user, name="subscribe"),
    path("posts/", litreviewapp.views.user_posts, name="posts"),
    path("subscribe/<int:pk>/", litreviewapp.views.unfollow_user, name="unfollowuser"),
    path("response_ticket/<int:pk>/", litreviewapp.views.response_ticket, name="responseticket"),
    path("feed/<int:pk>/delete_review", litreviewapp.views.delete_review, name="deletereview"),
    path("feed/<int:pk>/delete_ticket", litreviewapp.views.delete_ticket, name="deleteticket"),
    path("modify_review/<int:pk>/", litreviewapp.views.modify_review, name="modifyreview"),
    path("modify_ticket/<int:pk>/", litreviewapp.views.modify_ticket, name="modifyticket"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
