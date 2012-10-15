#!/usr/bin/env python

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from apscheduler.scheduler import Scheduler
from django.template.loader import render_to_string
from django.core.mail import *
from controllers.models import *
import datetime

sched = Scheduler()

sched.start()
@sched.interval_schedule(seconds=60)
def some_job():
    newslatter = Newslatter.objects.all()
    article = Article.objects.all()
    articles = []
    for i in article:
        if i.data >= datetime.date.today() and i.aprobat:
            articles.append(i)
    for j in newslatter:
        if j.active and j.data==datetime.date.today():
            message = EmailMultiAlternatives( "Nesletter","", settings.DEFAULT_FROM_EMAIL, [j.email]) 
            message.attach_alternative(render_to_string("newslatter.html",{'articles':articles,'ip':"http://109.96.205.31:8000"}),"text/html") 
            message.send() 
            print "Trimis"
    print "NeTrimis"
    #print render_to_string("newslatter.html",{'articles':articles});


while True:
    pass
