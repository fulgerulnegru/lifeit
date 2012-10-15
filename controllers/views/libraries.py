#din django
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext, Context
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.views import login
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import *
from django.core.mail import send_mail
from django.core.paginator import Paginator, InvalidPage
from django.template.loader import render_to_string
import os
import random
import datetime
#din site
from controllers.models import *
from controllers.forms import *

delete = os.path.join(os.path.dirname(__file__),'../../static')
delete = str(delete)
