from django import template


register = template.Library()

@register.simple_tag
def share_fb(article,user):
    if not article.share_fb.filter(user =user):
        return '<button class="btn btn-info share_fb" onclick="test(FB,' + str(article.id) + ',' + "'" + str(article.image) +"'" +')"><img src="/static/images/share_fb.jpg"></img> Share</button></br></br>'
    return ''

