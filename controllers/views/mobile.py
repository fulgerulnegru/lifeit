from libraries import *

ITEMS_PER_ARTICLES = 4

# well home
def home(request):
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

    return render_to_response("mobile/home.html",RequestContext(request,{'menu':menu,'articles':page,'articles_paginator':paginator.num_pages > 1,'articles_page_n':page_number,'page_n':page_n,
        'has_prev': page.has_previous(),'has_next': page.has_next(), 'page': page_number,'pages': paginator.num_pages,'next_page': page_number + 1,'prev_page': page_number - 1,"id":page_number,'link':link}))


#well for menu
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

    paginator = Paginator(menu2.articles.all(),ITEMS_PER_ARTICLES)
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

    menu = []
    for i in Menu.objects.order_by('order'):
        menu.append({'menu':i,'undermenu1':i.undermenu.order_by('order')})

    link = Links.objects.all()
    date =  datetime.date.today()

    return render_to_response("mobile/menu2.html",RequestContext(request,{'menu3':menu2,'menu2':page,'data':date,'menu':menu,'menu1':menu1,'url':url,'link':link,'articles_paginator':paginator.num_pages > 1,'articles_page_n':page_number,'page_n':page_n,
        'has_prev': page.has_previous(),'has_next': page.has_next(), 'page': page_number,'pages': paginator.num_pages,'next_page': page_number + 1,'prev_page': page_number - 1,"id":page_number}))


#well for article
def article_optimization(id):
    prev = ""
    next = ""
    articles = Article.objects.filter(aprobat=True).order_by('-data')
    n =  len(articles)
    i = list(articles.values_list('id',flat=True)).index(int(id))

    if i > 0 :
        prev = articles.values_list('id',flat=True)[i - 1]

    if i < n-1:
        next = articles.values_list('id',flat=True)[i + 1]

    return Context({'prev':prev,'next':next})


def article(request):
    if 'id' in request.GET:
        menu = []
        for i in Menu.objects.order_by('order'):
            menu.append({'menu':i,'undermenu1':i.undermenu.order_by('order')})

        link = Links.objects.all()

        id=request.GET["id"]
        article = Article.objects.get(id=id)

        return render_to_response("mobile/article.html",RequestContext(request,{'article':article,'menu':menu,'link':link}),article_optimization(id))


#well ajax
def article_ajax(request):
    if 'id' in request.GET:

        id=request.GET["id"]
        article = Article.objects.get(id=id)
        return render_to_response("mobile/ajax/article.html",RequestContext(request,{'article':article}),article_optimization(id))


def newsletter(request):
    if request.method == "POST":
        form = AddEmailForm(request.POST)
        if form.is_valid():
            try:
                email = Newslatter.objects.create(email=form.cleaned_data['email'],cod=random.randrange(10001, 100000))
                mesaj = "Linkul este pentru a finaliza abonarea http://"  + request.META.get('HTTP_HOST') + "/abonare/" + email.email + "/" + str(email.cod) 
                send_mail("Abonare", mesaj , "lifeit2013@gmail.com", [email.email]) 
                return render_to_response("ajax/email.html",RequestContext(request,{'form':form,'mesaj':"Verifica adresa de email pentru a te putea abona"}))
                return render_to_response("mobile/ajax/newsletter.html", RequestContext(request,{'form':form,'mesaj':"Verifica adresa de email pentru a te putea abona"}))
            except:
                email = Newslatter.objects.get(email=form.cleaned_data['email'])
                if not email.active:
                    mesaj = "Linkul este pentru a te abona http://"  + request.META.get('HTTP_HOST') + "/abonare/" + email.email + "/" + str(email.cod)
                    send_mail("Abonare", mesaj , "lifeit2013@gmail.com", [email.email])
                    return render_to_response("mobile/ajax/newsletter.html", RequestContext(request,{'form':form,'mesaj':"Email mai este in baza de date dar nu a fost activat asa ca se trimite un nou email"}))
                else:
                    return render_to_response("mobile/ajax/newsletter.html", RequestContext(request,{'form':form,'mesaj':"Email este in baza de date si activat"}))
    else:
        form = AddEmailForm()
    return render_to_response("mobile/ajax/newsletter.html", RequestContext(request,{'form':form}))



def login(request):
    error = ""
    message = ""
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(username = username,password = password)
        if user is not None:
            auth_login(request, user)
        else:
            error = "yes"
    else:
        form = UserLoginForm()
    return render_to_response("mobile/ajax/login.html", RequestContext(request,{'form':form,'error':error}))


