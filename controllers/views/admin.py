from libraries import *


@login_required
def home (request):
    return render_to_response("admin/profile.html",RequestContext(request))


@login_required
def edit_profile(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        form = UserModelForm(request.POST,instance=user)
        form1 = ProfileModelForm(request.POST,instance=profile)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            mesaj = "Sa modificat cu succes"
            return render_to_response("ajax/edit_profile.html",RequestContext(request,{'form':form,'form1':form1,'mesaj':mesaj}))

    else:
        form = UserModelForm(instance=user)
        form1 = ProfileModelForm(instance=profile)
    return render_to_response("ajax/edit_profile.html",RequestContext(request,{'form':form,'form1':form1}))


@login_required
@csrf_exempt
def upload_profile(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        profile = Profile.objects.get(user=user)
        text = str(profile.image)
        profile.image = request.FILES['image']
        profile.save()
        os.remove(delete + '/' + str(text) )
        os.system("mogrify -resize 200x200 "+ "'" + "static/" + str(profile.image) + "'")
    return HttpResponse('ok')


def edit_user(request):
    user_all = User.objects.all()
    return render_to_response("admin/edit_user.html",RequestContext(request,{'user_all':user_all}))


@login_required
def delete_user(request):
    if 'id' in request.GET:
        if request.user.is_staff:
            user = User.objects.get(id=request.GET['id'])
            if not user.is_staff:
                text = str(user.profile.image)
                user.delete()
                os.remove('static/' + str(text) )
            return HttpResponse('ok')


@login_required
def blocked_user(request):
    if 'id' in request.GET:
        if request.user.is_staff:
            user = User.objects.get(id=request.GET['id'])
            if not user.is_staff:
                if user.profile.blocked:
                    user.profile.blocked = 0
                    user.profile.save()
                else:
                    user.profile.blocked = 1
                    user.profile.save()
            return HttpResponse('ok')


@login_required
def add_user(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = AddUserForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(form.cleaned_data['username'],form.cleaned_data['email'])
                Profile.objects.create(user=user,cod=random.randrange(10001, 100000))
                mesaj = "Ai fost selectat sa faci parte din echipa de editori ai blogului Lifeit http://"  + request.META.get('HTTP_HOST') + "/active/" + user.username + "/" + str(user.profile.cod) 
                send_mail("Editor Lifeit", mesaj , "lifeit2013@gmail.com", [user.email]) 
                mesaj = "Sa creat cu succes user"
                form = AddUserForm()
                return render_to_response("ajax/add_user.html",RequestContext(request,{'form':form,'mesaj':mesaj}))
        else:
            form = AddUserForm()
        return render_to_response("ajax/add_user.html",RequestContext(request,{'form':form}))
