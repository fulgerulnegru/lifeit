from django.conf.urls import patterns, include, url
from controllers.views import *
import os
from django.shortcuts import redirect
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    #well views
    url(r'^$',views.home, name='home'),
    url(r'email/$',views.email, name='email'),
    url(r'views/article/$' , views.article , name="views.article"),
    url(r'menu2/(?P<menu1>[\w|\W]+)/(?P<url>[\w|\W]+)$',views.menu, name='menu2'),
    url(r'newslatter/$',views.newslatter, name='newslatter'),
    url(r'user/(?P<user>[\w|\W]+)/$',views.user, name='user'),

    #wall admin
    #wall user
    url(r'admin/$',admin.home , name='admin'),
    url(r'admin/edit_profile/$', admin.edit_profile , name='edit_profile'),
    url(r'admin/upload_profile$' , admin.upload_profile , name="upload_profile"),
    url(r'admin/edit_user$' , admin.edit_user , name="edit_user"),
    url(r'admin/delete_user/$', admin.delete_user , name="delete_user"),
    url(r'admin/blocked_user/$', admin.blocked_user , name="blocked_user"),
    url(r'admin/add_user/$', admin.add_user , name="add_user"),

    #wall links
    url(r'admin/links$' , links.links , name="links"),
    url(r'admin/add_links$' , links.add_links , name="add_links"),
    url(r'admin/delete_links/$', links.delete_links , name="delete_links"),
    url(r'admin/edit_links/$', links.edit_links , name="edit_links"),

    #wall menu
    url(r'admin/menu$', menu.menu , name="menu"),
    url(r'admin/add_menu$' , menu.add_menu , name="add_menu"),
    url(r'admin/add_under_menu/$' , menu.add_under_menu , name="add_under_menu"),
    url(r'admin/delete_menu/([\w|\W]+)/$', menu.delete_menu , name="delete_menu"),
    url(r'admin/moveu_menu/([\w|\W]+)/([\w|\W]+)/$', menu.move_menu , name="move_menu"),
    url(r'admin/edit_menu/([\w|\W]+)/', menu.edit_menu , name="edit_menu"),

    #wall page
    url(r'admin/page$', page.page , name="page"),
    url(r'admin/add_page$' , page.add_page , name="add_page"),
    url(r'admin/delete_page/$', page.delete_page , name="delete_page"),
    url(r'admin/edit_page/$' , page.edit_page , name="edit_page"),

    #wall articles
    url(r'admin/my_articles/$' , articles.my_articles , name="my_articles"),
    url(r'admin/approved_articles/$' , articles.approved_articles , name="approved_articles"),
    url(r'admin/all_articles/$' , articles.all_articles , name="all_articles"),
    url(r'admin/blocked_articles$' , articles.blocked_articles , name="blocked_articles"),
    url(r'admin/add_articles$' , articles.add_articles , name="add_articles"),
    url(r'admin/delete_article/$' , articles.delete_article , name="delete_article"),
    url(r'admin/edit_article/$' , articles.edit_article , name="edit_article"),

    #wall file
    url(r'admin/all_file/$' , file.file , name="file"),
    url(r'admin/my_file/$' , file.my_file , name="my_file"),
    url(r'admin/delete_file$' , file.delete_file , name="delete_file"),

    #wall tags
    url(r'admin/add_tags$' , articles.add_tags , name="add_tags"),
    url(r'admin/refres_tags/' , articles.refres_tags , name="refres_tags"),
    url(r'admin/delete_tags/' , articles.delete_tags , name="delete_tags"),

    #wall auth
    url(r'login/$', auth.login , name = 'login'),
    url(r'logout/$', auth.logout_page , name = 'logout'),
    url(r'admin/change_password$', auth.change_password , name = 'change_password'),
    url(r'blocked$' , auth.blocked , name = 'blocked'),
    url(r'active$' , auth.active , name = 'active' ),
    url(r'active/(?P<user>[\w|\W]+)/(?P<cod>(\d+))$', auth.active_user , name="active_user"),

    #stylesheet and javascript and images and upload
    url(r'static/(?P<path>[\w|\W]+)$','django.views.static.serve' ,{'document_root' : os.path.join(os.path.dirname(__file__),'static')},name="static"),
)
