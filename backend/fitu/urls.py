"""fitu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from rest_framework import routers
from fitu_backend import views as json_views
from dbview import views as html_views
from image_upload import views as upload_views
from rest_framework.authtoken import views as token_views

router = routers.DefaultRouter()
router.register(r'userviews', html_views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^users/$', json_views.user_list),
    url(r'^users/check-duplicate$', json_views.check_duplicate),
    url(r'^users/(?P<username>.+)/$', json_views.user_detail),
    url(r'^avatars/$', upload_views.AvatarUpload.as_view()),
    url(r'^api-token-auth/', token_views.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
