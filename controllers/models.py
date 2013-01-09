from django.db.models import *
from django.contrib.auth.models import User


class Profile (Model):
    cod = IntegerField()
    blocked = BooleanField()
    active = BooleanField()
    describe = TextField(max_length=400)
    image = ImageField(upload_to="user")
    user = OneToOneField(User)


class Newslatter (Model):
    cod = IntegerField()
    active = BooleanField(default=False)
    email = EmailField(unique=True)


class File (Model):
    #use 5242880 for a file with size maximum 50 mb
    file = FileField(upload_to='file')
    name = CharField(max_length=50)
    user = ForeignKey(User)


class Links (Model):
    url = URLField(null=True,unique=True)
    value = CharField(max_length=300)
    rel = CharField(max_length=50)


class Page (Model):
    title = CharField(max_length=200)
    body = TextField()


class Tag (Model):
    name = CharField(max_length=64, unique=True)


class Share_fb (Model):
    user =  ForeignKey(User)
    id_share = CharField(max_length=100,unique=True)


class Article (Model):
    title = CharField(max_length=200)
    describe = CharField(max_length=500)
    body = TextField()
    data = DateField()
    aprobat = BooleanField(default=False)
    image = ImageField(upload_to="article")
    tag = ManyToManyField(Tag,null=True)
    user = ForeignKey(User)
    share_fb = ManyToManyField(Share_fb,null=True)


class UnderMenu (Model):
    undermenu = CharField(max_length=50)
    page = OneToOneField(Page,null=True,on_delete=SET_NULL)
    articles = ManyToManyField(Article,null=True)
    url = CharField(max_length=50)
    order = IntegerField(null=True)


class Menu (Model):
    menu = CharField(max_length=50)
    undermenu = ManyToManyField(UnderMenu)
    page = OneToOneField(Page,null=True,on_delete=SET_NULL)
    articles = ManyToManyField(Article,null=True)
    url = CharField(max_length=50)
    order = IntegerField(null=True)
