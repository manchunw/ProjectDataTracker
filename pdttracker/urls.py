"""pdttracker URL Configuration

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
from django.contrib import admin
from pdttracker.views import home, auth_login, auth_logout, currentTime, table_view, project_view

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # following is tested by Kelvin
    # url(r'^$', 'pdttracker.views.home'),
    url(r'^$', 'pdttracker.views.auth_login'),
    url(r'^login/', 'pdttracker.views.auth_login'),
    url(r'^logout/', 'pdttracker.views.auth_logout'),
    url(r'^now/', 'pdttracker.views.currentTime'),
    url(r"^view/([a-zA-Z0-9_]+)/$", "pdttracker.views.table_view"),
    url(r'^project/', 'pdttracker.views.project_view'),
]
