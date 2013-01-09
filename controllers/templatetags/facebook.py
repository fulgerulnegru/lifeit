from libraries import *


@login_required
def login(request):
    facebook = Pyfb(FACEBOOK_APP_ID)
    return HttpResponseRedirect(facebook.get_auth_code_url(redirect_uri=FACEBOOK_REDIRECT_URL))


@login_required
def login_success(request):
    return HttpResponse("<script> window.location='/admin/my_articles/' </script>")


@login_required
def add_share(request):
    article = Article.objects.get(id=request.GET['id_article'])
    share = Share_fb.objects.create(user=request.user,id_share=request.GET['id_share'])
    article.share_fb.add(share)
    return HttpResponse("ok")
