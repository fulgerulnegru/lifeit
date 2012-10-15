from libraries import *

@login_required
def page(request):
    page = Page.objects.all()
    return render_to_response("admin/page.html",RequestContext(request,{'page':page}))


@login_required
def add_page(request):
    if request.user.is_staff:

        menu = []
        for i in Menu.objects.order_by('order'):
            menu.append({'menu':i,'undermenu1':i.undermenu.order_by('order')})

        if request.method =="POST":
            try:
                value = request.POST['menu']
            except:
                value = ""
            form = AddPageForm(request.POST)

            if form.is_valid() and value:
                i=0
                while(i<len(value)):
                    order = value[i]
                    i+=1

                if value[0] == "i":
                    menu1 = UnderMenu.objects.get(order=order)
                else:
                    menu1 = Menu.objects.get(order=order)

                page = Page.objects.create(title= form.cleaned_data['title'],body=form.cleaned_data['body'])
                menu1.page = page
                menu1.save()
                value = ""
                form = AddPageForm()
                return render_to_response("admin/add_page.html",RequestContext(request,{'value':"",'menu':menu,'form':form,'mesaj':"Sa creat cu succes pagina"}))

            error= "<ul class='errorlist'><li>This field is required.</li></ul>"
            return render_to_response("admin/add_page.html",RequestContext(request,{'value':value,'menu':menu,'form':form,'error':error}))
        else:
            form = AddPageForm()
        return render_to_response("admin/add_page.html",RequestContext(request,{'menu':menu,'form':form}))


@login_required
def edit_page(request):
    if request.user.is_staff:
        if 'id' in request.GET:
            id = request.GET['id']
            page = Page.objects.get(id = id)
            val_menu = ""
            value = ""

            try:
                page.undermenu
                value = "i"
                val_menu = page.undermenu
                value += str(page.undermenu.order)
            except:
                pass
            try:
                page.menu
                value = "m"
                val_menu = page.menu
                value += str(page.menu.order)
            except:
                pass

            value1 = value

            menu = []
            for i in Menu.objects.order_by('order'):
                menu.append({'menu':i,'undermenu1':i.undermenu.order_by('order')})

            if request.method == "POST":
                error = ""
                try:
                    value = request.POST['menu']
                except:
                    value = ""
                if  not value :
                    error= "<ul class='errorlist'><li>This field is required.</li></ul>"
                form = EditPageModelForm(request.POST,instance=page)

                if form.is_valid() and value:
                    i=0;
                    while(i<len(value)):
                        order = value[i]
                        i+=1

                    if value[0] == "i":
                        menu1 = UnderMenu.objects.get(order=order)
                    else:
                        menu1 = Menu.objects.get(order=order)

                    try:
                        val_menu.page.delete()
                    except:
                        pass
                    menu1.page = page
                    menu1.save()
                    form.save()
                    page = Page.objects.get(id=id)
                    menu = []
                    for i in Menu.objects.order_by('order'):
                        menu.append({'menu':i,'undermenu1':i.undermenu.order_by('order')})

                    return render_to_response("admin/edit_page.html",RequestContext(request,{'value':value,'page':page,'menu':menu,'form':form,'id':id,'mesaj':"Sa modificat cu succes pagina"}))

                if not value:
                    return render_to_response("admin/edit_page.html",RequestContext(request,{'value':value,'page':page,'menu':menu,'form':form,'id':id,'error':error}))
            else:
                form = EditPageModelForm(instance = page)

            return render_to_response("admin/edit_page.html",RequestContext(request,{'value':value,'page':page,'menu':menu,"form":form,'id':id}))


@login_required
def delete_page(request):
    if 'id' in request.GET:
        if request.user.is_staff:
            Page.objects.get(id=request.GET["id"]).delete()
            return HttpResponse('ok')
