from libraries import *

ITEMS_PER_FILE = 20


@login_required
def file(request):
    file = File.objects.order_by("-id")
    paginator = Paginator(file,ITEMS_PER_FILE)
    try:
        page_number = int(request.GET['page'])
    except (KeyError, ValueError):
        page_number = 1
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        page = paginator.page(1)
    if request.method == "POST":
        form = FileForm(request.POST,request.FILES)
        if form.is_valid():
            File.objects.create(user=request.user,file=form.cleaned_data['file'],name=str(form.cleaned_data['file']))
            return redirect("/admin/all_file")
    else:
        form = FileForm()
    return render_to_response("admin/file.html",RequestContext(request,{'form':form,"file":page,'file_paginator':paginator.num_pages > 1,'has_prev': page.has_previous(),'has_next': page.has_next(),
            'page': page_number,'pages': paginator.num_pages,'next_page': page_number + 1,'prev_page': page_number - 1,"id":page_number}))


@login_required
def my_file(request):
    file = File.objects.filter(user=request.user).order_by("-id")
    paginator = Paginator(file,ITEMS_PER_FILE)
    try:
        page_number = int(request.GET['page'])
    except (KeyError, ValueError):
        page_number = 1
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        page = paginator.page(1)
    if request.method == "POST":
        form = FileForm(request.POST,request.FILES)
        if form.is_valid():
            File.objects.create(user=request.user,file=form.cleaned_data['file'],name=str(form.cleaned_data['file']))
            return redirect("/admin/my_file")
    else:
        form = FileForm()
    return render_to_response("admin/my_file.html",RequestContext(request,{'form':form,"file":page,'file_paginator':paginator.num_pages > 1,'has_prev': page.has_previous(),'has_next': page.has_next(),
            'page': page_number,'pages': paginator.num_pages,'next_page': page_number + 1,'prev_page': page_number - 1,"id":page_number}))


@login_required
def delete_file(request):
    if 'id' in request.GET:
        if request.user.is_staff:
            file = File.objects.get(id=request.GET["id"])
            os.remove(delete + "/" + str(file.file))
            file.delete()
            return HttpResponse("ok")
        else:
            try:
                file = File.objects.filter(user = request.user).get(id=request.GET["id"])
                os.remove("static/" + str(file.file))
                file.delete()
                return HttpResponse("ok")
            except:
                return Http404()
