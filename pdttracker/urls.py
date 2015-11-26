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
from pdttracker import views
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # following is tested by Kelvin
    # url(r'^$', 'pdttracker.views.home'),
    url(r'^$', 'pdttracker.views.auth_login'),
    url(r'^login/', 'pdttracker.views.auth_login'),
    url(r'^logout/', 'pdttracker.views.auth_logout'),
    url(r'^now/', 'pdttracker.views.currentTime'),
    url(r'^selectMode/(?P<pk>[0-9]+)/', 'pdttracker.views.selectMode', name='selectMode'),
    url(r'^developmentMode/(?P<pk>[0-9]+)/', 'pdttracker.views.developmentMode'),
    url(r"^view/([a-zA-Z0-9_]+)/$", "pdttracker.views.table_view"),
    url(r'^project/', 'pdttracker.views.project_view', name='project_view'),
    url(r'^project_form/', 'pdttracker.views.addProject', name='addProject'),
    # url(r'^editProject/(?P<pk>[0-9]+)/', 'pdttracker.views.editProject', name='editProject'),
    url(r'^iteration_form/', 'pdttracker.views.addIteration', name='addIteration'),
    url(r'^editIteration/(?P<pk>[0-9]+)/', 'pdttracker.views.editIteration', name='editIteration'),
    url(r'^iteration/', 'pdttracker.views.iteration_view', name='iteration_view'),
    url(r'^defect_form/(?P<pk>[0-9]+)/', views.addDefect.as_view(), name='addDefect'),
    url(r'^editDefect/(?P<pk>[0-9]+)/', views.editDefect.as_view(), name='editDefect'),
    url(r'^defect/', 'pdttracker.views.defect_view', name='defect_view'),
    url(r'^welcomeHR/', 'pdttracker.views.welcomeHR', name='welcomeHR'),
    url(r'^welcomeAdmin/', 'pdttracker.views.welcomeAdmin', name='welcomeAdmin'),
    url(r'^modifyProject/(?P<pk>[0-9]+)/', 'pdttracker.views.modifyProject', name='modifyProject'),
    url(r"^report/(?P<reporttype>[a-zA-Z0-9_]+)/(?P<pk>[0-9_]+)/$", "pdttracker.views.report_view"),
    url(r'^project_detail/(?P<pk>[0-9]+)/', 'pdttracker.views.project_detail', name='project_detail'),
    url(r'^defect_detail/(?P<pk>[0-9]+)/', 'pdttracker.views.defect_detail', name='defect_detail'),
    url(r'^create_user/', views.create_user.as_view()),
    url(r'^edit_user/(?P<pk>[0-9]+)/', views.edit_user.as_view()),
    url(r'^staff_view/', 'pdttracker.views.staff_view', name='staff_view'),
    url(r"^switch_project/(?P<pk>[0-9]+)/", "pdttracker.views.switch_project"),
    url(r'^view_defect/(?P<pk>[0-9]+)/', 'pdttracker.views.defect_view', name='defect_view'),
    url(r'^api/(?P<command>[a-zA-Z0-9_]+)/(?P<pk>[0-9]+)/', 'pdttracker.views.api_call', name='api_call'),
    url(r'^editProject/(?P<pk>[0-9]+)/', views.editProject.as_view(), name='editProject'),

]
