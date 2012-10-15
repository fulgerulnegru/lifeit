from libraries import *

# din motive ca sar complica proiectul am lasat id in undele locuri in reuqest.Get in loc de order
# de lucru la nivelul de order si de rezolvare a definiri order in baza de date

@login_required
def menu(request):
    menu = []
    for i in Menu.objects.order_by('order'):
        menu.append({'menu':i,'undermenu1':i.undermenu.order_by('order')})
    return render_to_response("admin/menu.html",RequestContext(request,{'menu':menu}))


@login_required
def add_menu(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = AddMenuForm(request.POST)
            if form.is_valid():
                menu = Menu.objects.create(menu=form.cleaned_data['menu'],url=form.cleaned_data['url'])
                order = Menu.objects.order_by('-order')[0]
                if not order.order:
                    order.order = 0
                menu.order = order.order + 1 
                menu.save()
                mesaj = "Sa creat cu succes"
                form = AddMenuForm()
                return render_to_response("ajax/add_menu.html",RequestContext(request,{'form':form,'mesaj':mesaj}))
        else:
            form = AddMenuForm()
    return render_to_response("ajax/add_menu.html",RequestContext(request,{'form':form}))


@login_required
def add_under_menu(request):
    if 'id' in request.GET:
        id = request.GET['id']
        menu = Menu.objects.get(order=id)
        if request.user.is_staff:
            if request.method == "POST":
                form = AddUnderMenuForm(request.POST)
                if form.is_valid():
                    undermenu = UnderMenu.objects.create(undermenu=form.cleaned_data['undermenu'],url=form.cleaned_data['url'])
                    order = UnderMenu.objects.order_by('-order')[0]
                    if not order.order:
                        order.order = 0
                    undermenu.order = order.order + 1 
                    undermenu.save()
                    menu.undermenu.add(undermenu)
                    mesaj = "Sa creat cu succes"
                    form = AddUnderMenuForm()
                    return render_to_response("ajax/add_under_menu.html",RequestContext(request,{'form':form,'id':id,'mesaj':mesaj,"menu":menu}))
            else:
                form = AddUnderMenuForm()
        return render_to_response("ajax/add_under_menu.html",RequestContext(request,{'form':form,'id':id,"menu":menu}))


@login_required
def delete_menu(request,option):
    if request.user.is_staff:
        if 'id' in request.GET:
            id = request.GET['id']
            if option == "menu":
                menu = Menu.objects.get(order=id)
                menu.undermenu.all().delete()
                menu.delete()
            elif option == "undermenu":
                undermenu = UnderMenu.objects.get(order=id)
                undermenu.delete()
            return HttpResponse("ok")


@login_required
def move_menu(request,direction , option):
    if request.user.is_staff:
        if 'order' in request.GET:
            order = request.GET['order']
            if option == "menu":
                menu = Menu.objects.get(order=order)
                if direction == "up":
                    order = int(order) - 1
                    menu1 = Menu.objects.get(order=order)
                elif direction == "down":
                    order = int(order) + 1
                    menu1 = Menu.objects.get(order=order)
            elif option == "undermenu":
               menu = UnderMenu.objects.get(order=order)
               if direction == "up":
                    order = int(order) - 1
                    menu1 = UnderMenu.objects.get(order=order)
               if direction == "down":
                    order = int(order) + 1
                    menu1 = UnderMenu.objects.get(order=order)

            menu1.order , menu.order = menu.order , menu1.order
            menu.save()
            menu1.save()
        return HttpResponse("ok")


@login_required
def edit_menu(request,option):
    if request.user.is_staff:
        if 'order' in request.GET:
            order = request.GET['order']
        if option == "menu":
            menu = Menu.objects.get(order=order)
            if request.method == "POST":
                form = AddMenuModelForm(request.POST,instance=menu)
                if form.is_valid():
                    form.save()
                    mesaj = "Sa editat cu succes"
                    return render_to_response("ajax/edit_menu.html",RequestContext(request,{'form':form,'mesaj':mesaj,'value':"Edit menu",'url':'/admin/edit_menu/'+option+'/?order='+str(menu.order)}))
            else:
                form = AddMenuModelForm(instance=menu)
            return render_to_response("ajax/edit_menu.html",RequestContext(request,{'form':form,'value':"Edit menu",'url':'/admin/edit_menu/'+option+'/?order='+str(menu.order)}))

        elif option == "undermenu":
            menu = UnderMenu.objects.get(order=order)
            if request.method == "POST":
                form = AddUnderMenuModelForm(request.POST,instance=menu)
                if form.is_valid():
                    form.save()
                    mesaj = "Sa editat cu succes"
                    return render_to_response("ajax/edit_menu.html",RequestContext(request,{'form':form,'mesaj':mesaj,'value':"Edit menu",'url':'/admin/edit_menu/'+option+'/?order='+str(menu.order)}))
            else:
                form = AddUnderMenuModelForm(instance=menu)
            return render_to_response("ajax/edit_menu.html",RequestContext(request,{'form':form,'value':"Edit menu",'url':'/admin/edit_menu/'+option+'/?order='+str(menu.order)}))
