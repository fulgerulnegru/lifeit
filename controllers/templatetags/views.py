from libraries import *

ITEMS_PER_ARTICLES = 20


def feed(request):
    articles = Article.objects.filter(aprobat = True).order_by('-data')[:10]
    f = feedgenerator.Atom1Feed( title=u"Lifeit",link=u"http://lifeit.ro",description=u"Este un blog dedicat programari si tot ce tine de informatica.",
            language=u"ro",author_name=u"Lifeit",feed_url=u"http://http://lifeit.ro/feed")

    for i in articles:
        f.add_item(title=i.title,link=u"http://lifeit.ro//views/article/?id="+str(i.id),pubdate=i.data,description=i.body)
    return HttpResponse(f.writeString('UTF-8'),content_type="application/xhtml+xml")


def home (request):
    menu = []
    article = []

    for i in Menu.objects.order_by('order'):
        menu.append({'menu':i,'undermenu1':i.undermenu.order_by('order')})

    articles = Article.objects.order_by("-data")
    for i in articles:
        if i.data <= datetime.date.today() and i.aprobat:
            article.append(i)

    articles = article

    paginator = Paginator(articles,ITEMS_PER_ARTICLES)
    try:
        page_number = int(request.GET['page'])
        page_n = True
    except (KeyError, ValueError):
        page_number = 1
        page_n = False
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        page = paginator.page(1)

    link = Links.objects.all()

    return render_to_response("home.html",RequestContext(request,{'link':link,'menu':menu,"articles":page,'articles_paginator':paginator.num_pages > 1,'articles_page_n':page_number,'page_n':page_n,
        'has_prev': page.has_previous(),'has_next': page.has_next(), 'page': page_number,'pages': paginator.num_pages,'next_page': page_number + 1,'prev_page': page_number - 1,"id":page_number}))


def email(request):
    if request.method == "POST":
        form = AddEmailForm(request.POST)
        if form.is_valid():
            try:
                email = Newslatter.objects.create(email=form.cleaned_data['email'],cod=random.randrange(10001, 100000))
                mesaj = "Linkul este pentru a finaliza abonarea http://"  + request.META.get('HTTP_HOST') + "/abonare/" + email.email + "/" + str(email.cod) 
                send_mail("Abonare", mesaj , "lifeit2013@gmail.com", [email.email]) 
                return render_to_response("ajax/email.html",RequestContext(request,{'form':form,'mesaj':"Verifica adresa de email pentru a te putea abona"}))
            except:
                email = Newslatter.objects.get(email=form.cleaned_data['email'])
                if not email.active:
                    mesaj = "Linkul este pentru a te abona http://"  + request.META.get('HTTP_HOST') + "/abonare/" + email.email + "/" + str(email.cod) 
                    send_mail("Abonare", mesaj , "lifeit2013@gmail.com", [email.email]) 
                    return render_to_response("ajax/email.html",RequestContext(request,{'form':form,'mesaj':"Email mai este in baza de date dar nu a fost activat asa ca se trimite un nou email "}))
                else:
                    return render_to_response("ajax/email.html",RequestContext(request,{'form':form,'mesaj':"Email este in baza de date si activat"}))
    else:
        form = AddEmailForm()
    return render_to_response("ajax/email.html",RequestContext(request,{'form':form}))


def article(request):
    if 'id' in request.GET:
        menu = []
        for i in Menu.objects.order_by('order'):
            menu.append({'menu':i,'undermenu1':i.undermenu.order_by('order')})

        link = Links.objects.all()

        id=request.GET["id"]
        article = Article.objects.get(id=id)

        return render_to_response("article.html",RequestContext(request,{'article':article,'menu':menu,'link':link}))


def menu(request,menu1,url):
    if menu1 == "menu":
        try:
            menu2 = Menu.objects.get(url=url)
        except:
            return Http404()
    if menu1 == "undermenu":
        try:
            menu2 = UnderMenu.objects.get(url=url)
        except:
            return Http404()
    menu = []
    for i in Menu.objects.order_by('order'):
        menu.append({'menu':i,'undermenu1':i.undermenu.order_by('order')})

    link = Links.objects.all()
    date =  datetime.date.today()

    return render_to_response("menu1.html",RequestContext(request,{'menu2':menu2,'data':date,'menu':menu,'menu1':menu1,'url':url,'link':link}))


def newslatter(request):
    article = Article.objects.all()
    articles = []
    for i in article:
        if i.data == datetime.date.today() and i.aprobat:
            articles.append(i)
    return render_to_response("newslatter.html",{'articles':articles,'ip':"http://lifeit.ro",'data':datetime.date.today()})


def user(request):
    pass


def email_a(request,abonare,email,cod):
    try:
        email = Newslatter.objects.get(email=email,cod=cod)
        menu = []
        article = []
        for i in Menu.objects.order_by('order'):
            menu.append({'menu':i,'undermenu1':i.undermenu.order_by('order')})

        articles = Article.objects.order_by("-data")
        for i in articles:
            if i.data <= datetime.date.today() and i.aprobat:
                article.append(i)
        link = Links.objects.all()

        if abonare == "abonare":
            email.active = True
            email.save()
            return render_to_response("abonare.html",RequestContext(request,{'menu':menu,'articles':article,'link':link,'message':"Ai fost abonat cu succes"}))
        if abonare == "dezabonare":
            email.delete()
            return render_to_response("abonare.html",RequestContext(request,{'menu':menu,'articles':article,'link':link,'message':"Ai fost dezabonat cu succes "}))
    except:
        return Http404()

def newslatter_a(request,data):
    menu = []
    article = []
    for i in Menu.objects.order_by('order'):
        menu.append({'menu':i,'undermenu1':i.undermenu.order_by('order')})

    articles = Article.objects.order_by("-data")
    for i in articles:
        if i.data <= datetime.date.today() and i.aprobat:
            article.append(i)
    link = Links.objects.all()

    return render_to_response("newslatter_a.html",RequestContext(request,{'menu':menu,'articles':article,'link':link,'data':data}))


def robot(request):
    return HttpResponse("");
