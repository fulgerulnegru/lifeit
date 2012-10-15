from libraries import *

ITEMS_PER_ARTICLES = 20

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
            email = Newslatter.objects.create(email=form.cleaned_data['email'],cod=random.randrange(10001, 100000))
            mesaj = "Linkul este pentru a finaliza abonarea http://"  + request.META.get('HTTP_HOST') + "/abonare/" + email.email + "/" + str(email.cod) 
            send_mail("Abonare", mesaj , "lifeit2013@gmail.com", [email.email]) 
            return render_to_response("ajax/email.html",RequestContext(request,{'form':form,'mesaj':"Verifica adresa de email pentru a te putea abona"}))
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

    return render_to_response("menu1.html",RequestContext(request,{'menu2':menu2,'data':date,'menu':menu,'link':link}))


def newslatter(request):
    article = Article.objects.all()
    articles = []
    for i in article:
        if i.data == datetime.date.today() and i.aprobat:
            articles.append(i)
    return render_to_response("newslatter.html",{'articles':articles,'ip':"http://10.81.122.30:8000"})


def user(request):
    pass
