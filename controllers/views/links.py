from libraries import *

@login_required
def links(request):
    links = Links.objects.all()
    return render_to_response("admin/links.html",RequestContext(request,{'links':links}))


@login_required
def add_links(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = AddLinksForm(request.POST)
            if form.is_valid():
                Links.objects.create(rel=form.cleaned_data['rel'],url=form.cleaned_data['url'],value=form.cleaned_data['value'])
                mesaj = "Sa creat cu succes"
                form = AddLinksForm()
                return render_to_response("ajax/add_links.html",RequestContext(request,{'form':form,'mesaj':mesaj}))
        else:
            form = AddLinksForm()
    return render_to_response("ajax/add_links.html",RequestContext(request,{'form':form}))


@login_required
def delete_links(request):
    if 'id' in request.GET:
        if request.user.is_staff:
            links = Links.objects.get(id=request.GET['id'])
            links.delete()
            return HttpResponse('ok')


@login_required
def edit_links(request):
    if 'id' in request.GET:
        if request.user.is_staff:
            id = request.GET['id']
            links = Links.objects.get(id=id)
            if request.method == "POST":
                form = EditLinksModelForm(request.POST , instance = links )
                if form.is_valid():
                    form.save()
                    mesaj = "Sa modificat cu succes"
                    return render_to_response("ajax/edit_links.html",RequestContext(request,{'form':form,'mesaj':mesaj,'id':id}))
            else:
                form = EditLinksModelForm(instance = links)
            return render_to_response("ajax/edit_links.html",RequestContext(request,{'form':form,'id':id}))
