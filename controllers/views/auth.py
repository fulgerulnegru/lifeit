from libraries import *


@csrf_exempt
def login (request):
    error = ""
    message = ""
    if request.method=="POST":
            form = UserLoginForm(request.POST)
            username=request.POST["username"]
            password=request.POST["password"]
            user=authenticate(username = username,password = password)
            if user is not None:
                auth_login(request, user)
                message = "yes"
            else:
                error = "yes"
    else:
            form=UserLoginForm()
    return render_to_response("ajax/login.html",RequestContext(request,{"login_form":form,'error':error,'message':message}))


@login_required
def logout_page (request):
    logout(request)
    return redirect('/')


@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user,password=form.cleaned_data['password'])
            if user == None:
                error = '<ul class="errorlist"><li>Parola veche nu e buna</li></ul>'
                return render_to_response("admin/change_password.html", RequestContext(request,{'form':form,'error':error}))
            else:
                user.set_password(form.cleaned_data['password1'])
                user.save()
                message = '<ul class="errorlist"><li>Sa modificat cu succes</li></ul>'
                return render_to_response("admin/change_password.html", RequestContext(request,{'form':form,'message':message}))
    else:
        form = ChangePasswordForm()
    return render_to_response("admin/change_password.html", RequestContext(request,{'form':form}))


@login_required
def blocked(request):
    pass


@login_required
def active(request):
    pass


def active_user(request,user,cod):
    if request.method == "POST":
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=user)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            cod = int(cod)
            if user.profile.cod == cod and not user.profile.active:
                user.profile.active = True
                user.profile.save()
                return redirect("/")
            else:
                return Http404
                pass
    else:
        form = SetPasswordForm()
    return render_to_response("admin/active_user.html",RequestContext(request,{"form":form}))

