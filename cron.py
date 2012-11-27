#!/usr/bin/env python


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.mail import *
from controllers.models import *
import datetime
from django.template.loader import render_to_string

def some_job():
    newslatter = Newslatter.objects.all()
    article = Article.objects.all()
    articles = []
    for i in article:
        if i.data == datetime.date.today() and i.aprobat:
            articles.append(i)
    if articles:
        for j in newslatter:
            if j.active:
                message = EmailMultiAlternatives( "Neswletter","", settings.DEFAULT_FROM_EMAIL, [j.email]) 
                message1 =  render_to_string("newslatter.html",{'articles':articles,'ip':"http://lifeit.ro",'data':datetime.date.today(),'j':j})
                message.attach_alternative(message1,"text/html") 
                message.send() 

some_job()
