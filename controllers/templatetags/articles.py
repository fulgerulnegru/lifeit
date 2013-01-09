from libraries import *

ITEMS_PER_TAGS = 8
ITEMS_PER_ARTICLES = 10


@login_required
def my_articles(request):
    articles = Article.objects.filter(user=request.user).order_by("-data")
    paginator = Paginator(articles,ITEMS_PER_ARTICLES)
    try:
        page_number = int(request.GET['page'])
    except (KeyError, ValueError):
        page_number = 1
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        page = paginator.page(1)
    return render_to_response("admin/articles.html",RequestContext(request,{"FACEBOOK_APP_ID": FACEBOOK_APP_ID,"articles":page,'articles_paginator':paginator.num_pages > 1,'has_prev': page.has_previous(),'has_next': page.has_next(),
        'page': page_number,'pages': paginator.num_pages,'next_page': page_number + 1,'prev_page': page_number - 1,"id":page_number}))


@login_required
def approved_articles(request):
    if request.user.is_staff:
        articles = Article.objects.filter(aprobat = False).order_by("-data")
        paginator = Paginator(articles,ITEMS_PER_ARTICLES)
        try:
            page_number = int(request.GET['page'])
        except (KeyError, ValueError):
            page_number = 1
        try:
            page = paginator.page(page_number)
        except InvalidPage:
            page = paginator.page(1)
        return render_to_response("admin/approved_articles.html",RequestContext(request,{"articles":page,'articles_paginator':paginator.num_pages > 1,'has_prev': page.has_previous(),'has_next': page.has_next(),
            'page': page_number,'pages': paginator.num_pages,'next_page': page_number + 1,'prev_page': page_number - 1,"id":page_number}))


@login_required
def all_articles(request):
    articles = Article.objects.order_by("-data")
    paginator = Paginator(articles,ITEMS_PER_ARTICLES)
    try:
        page_number = int(request.GET['page'])
    except (KeyError, ValueError):
        page_number = 1
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        page = paginator.page(1)
    return render_to_response("admin/all_articles.html",RequestContext(request,{"FACEBOOK_APP_ID": FACEBOOK_APP_ID,"articles":page,'articles_paginator':paginator.num_pages > 1,'has_prev': page.has_previous(),'has_next': page.has_next(),
        'page': page_number,'pages': paginator.num_pages,'next_page': page_number + 1,'prev_page': page_number - 1,"id":page_number}))


@login_required
def blocked_articles(request):
    if request.user.is_staff:
        if 'id' in request.GET:
            id = request.GET["id"]
            try:
                articles = Article.objects.get(id=id)
                if articles.aprobat:
                    articles.aprobat = False
                else:
                    articles.aprobat = True
                articles.save()
                return HttpResponse("OK")
            except:
                pass


def refres_tags_s(request):
    tags = Tag.objects.order_by("-id")
    paginator = Paginator(tags, ITEMS_PER_TAGS)
    try:
        page_number = int(request.GET['page'])
    except (KeyError, ValueError):
        page_number = 1
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        page = paginator.page(1)
    return render_to_string("ajax/refres_tags.html",RequestContext(request,{"tags":page,'tags_paginator':paginator.num_pages > 1,'has_prev': page.has_previous(),'has_next': page.has_next(),
        'page': page_number,'pages': paginator.num_pages,'next_page': page_number + 1,'prev_page': page_number - 1,"id":page_number}))


@login_required
def add_articles(request):
    menu = []
    for i in Menu.objects.order_by('order'):
        menu.append({'menu':i,'undermenu1':i.undermenu.order_by('order')})
    if request.method == "POST":
        error = ""
        error_t = ""
        try:
            value = request.POST['menu']
        except:
            value = ""
        error = ""
        try:
            value_t = request.POST['tags']
        except:
            value_t = ""

        tags = []
        nr = 0
        b = False
        for i in value_t:
            if i != " ":
                nr = nr*10 + int(i)
                b = True
            else:
                try:
                    tag = Tag.objects.get(id=nr)
                    tags.append(tag)
                except:
                    pass
                nr = 0

        try:
            tag = Tag.objects.get(id=nr)
            tags.append(tag)
        except:
            pass
        if not b:
            value_t = ""

        form = AddArticlesForm(request.POST,request.FILES)

        if form.is_valid() and value and value_t :
            i=0
            while(i<len(value)):
                order = value[i]
                i+=1

            if value[0] == "i":
                menu1 = UnderMenu.objects.get(order=order)
            else:
                menu1 = Menu.objects.get(order=order)

            article = Article.objects.create(title= form.cleaned_data['title'],describe=form.cleaned_data['describe'],body=form.cleaned_data['body'],data=form.cleaned_data['data'],user=request.user)
            article.image = form.cleaned_data['image']

            article.save()
            menu1.articles.add(article)
            for i in tags:
                article.tag.add(i)
            os.system("mogrify -resize 80x80 "+ "'" + delete + "/" + str(article.image) + "'")
            value = ""
            value_t = ""
            tags = ""
            form = AddArticlesForm()
            return render_to_response("admin/add_articles.html",RequestContext(request,{'tags':tags,'value_t':value_t,'refres_tags':refres_tags_s(request),'form':form,'value':value,'menu':menu,'mesaj':"Sa adaugat cu succes"}))
        if not value:
            error= "<ul class='errorlist'><li>This field is required.</li></ul>"
        if not value_t:
            error_t = "<ul class='errorlist'><li>This field is required.</li></ul>"
        return render_to_response("admin/add_articles.html",RequestContext(request,{'error_t':error_t,'tags':tags,'value_t':value_t,'refres_tags':refres_tags_s(request),'form':form,'menu':menu,'value':value,'error':error}))
    else:
        form = AddArticlesForm()
    return render_to_response("admin/add_articles.html",RequestContext(request,{'refres_tags':refres_tags_s(request),'form':form,'menu':menu}))


@login_required
def edit_article(request):
    if 'id' in request.GET:
        id = request.GET['id']
        menu = []
        val_menu = ""
        value = ""
        value_t = ""

        if request.user.is_staff:
            articles = Article.objects.get(id=id)
        else:
            try:
                articles = Article.objects.filter(user = request.user).get(id=id)
            except:
                return Http404()
        tags = articles.tag.all()
        for i in tags:
            value_t += " " + str(i.id)
        try:
            value = "i"
            val_menu = articles.undermenu_set.all()
            for i in articles.undermenu_set.all():
                value += str(i.order)
        except:
            pass

        try:
            if articles.menu_set.all():
                value = "m"
                val_menu = articles.menu_set.all()
                for i in articles.menu_set.all():
                    value += str(i.order)
        except:
            pass
        if len(value) == 1:
            value = ""
        value1 = value

        for i in Menu.objects.order_by('order'):
            menu.append({'menu':i,'undermenu1':i.undermenu.order_by('order')})

        if request.method == "POST":
            error = ""
            error_t = ""
            try:
                value = request.POST['menu']
            except:
                value = ""
            error = ""
            try:
                value_t = request.POST['tags']
            except:
                value_t = ""
            tags = []
            nr = 0
            b = False
            for i in value_t:
                if i != " ":
                    nr = nr*10 + int(i)
                    b = True
                else:
                    try:
                        tag = Tag.objects.get(id=nr)
                        tags.append(tag)
                    except:
                        pass
                    nr = 0
            try:
                tag = Tag.objects.get(id=nr)
                tags.append(tag)
            except:
                pass

            form = EditArticlesModelForm(request.POST,instance=articles)

            if form.is_valid() and value and value_t :
                i=0;
                while(i<len(value)):
                    order = value[i]
                    i+=1

                if value[0] == "i":
                    menu1 = UnderMenu.objects.get(order=order)
                else:
                    menu1 = Menu.objects.get(order=order)
                articles = Article.objects.get(id=id)

                try:
                    articles.menu_set.clear()
                except:
                    pass
                try:
                    articles.undermenu_set.clear()
                except:
                    pass
                menu1.articles.add(articles)
                menu1.save()
                form.save()
                articles.tag.clear()
                for i in tags:
                    articles.tag.add(i)

                return render_to_response("admin/edit_articles.html",RequestContext(request,{'id':id,'tags':tags,'value_t':value_t,'refres_tags':refres_tags_s(request),'form':form,'value':value,'menu':menu,'mesaj':"Sa editat cu succes"}))
            if not value:
                error= "<ul class='errorlist'><li>This field is required.</li></ul>"
            if not value_t:
                error_t = "<ul class='errorlist'><li>This field is required.</li></ul>"
            return render_to_response("admin/edit_articles.html",RequestContext(request,{'id':id,'error_t':error_t,'tags':tags,'value_t':value_t,'refres_tags':refres_tags_s(request),'form':form,'menu':menu,'value':value,'error':error}))
        else:
            form = EditArticlesModelForm(instance=articles)
        return render_to_response("admin/edit_articles.html",RequestContext(request,{'id':id,'tags':tags,'value_t':value_t,'refres_tags':refres_tags_s(request),'form':form,'value':value,'menu':menu}))


@login_required
def delete_article(request):
    if 'id' in request.GET:
        if request.user.is_staff:
            articles = Article.objects.get(id=request.GET["id"])
            if articles.image:
                os.remove(delete + '/'+str(articles.image))
            articles.delete()
            return HttpResponse("ok")
        else:
            try:
                articles = Article.objects.filter(user = request.user).get(id=request.GET["id"])
                if articles.image:
                    os.remove(delete + '/'+str(articles.image))
                articles.delete()
                return HttpResponse("ok")
            except:
                return Http404()


@login_required
def add_tags(request):
    if request.method == "POST":
        form = AddTagForm(request.POST)
        if form.is_valid():
            mesaj = "Sa creat cu succes tag-ul"
            try:
                Tag.objects.create(name = form.cleaned_data['name'])
            except:
                mesaj="Tag mai exista"
            form = AddTagForm()
            return render_to_response("ajax/add_tags.html",RequestContext(request,{'form':form,'mesaj':mesaj}))
    else:
        form = AddTagForm()
    return render_to_response("ajax/add_tags.html",RequestContext(request,{'form':form}))


def refres_tags(request):
    tags = Tag.objects.order_by("-id")
    paginator = Paginator(tags, ITEMS_PER_TAGS)
    try:
        page_number = int(request.GET['page'])
    except (KeyError, ValueError):
        page_number = 1
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        page = paginator.page(1)
    return render_to_response("ajax/refres_tags.html",RequestContext(request,{"tags":page,'tags_paginator':paginator.num_pages > 1,'has_prev': page.has_previous(),'has_next': page.has_next(),
        'page': page_number,'pages': paginator.num_pages,'next_page': page_number + 1,'prev_page': page_number - 1,'id':page_number}))


@login_required
def delete_tags(request):
    if 'id' in request.GET:
        Tag.objects.get(id=request.GET["id"]).delete()
    return HttpResponse("ok")
