from django.http import HttpResponse, JsonResponse
from django.urls import include, path
from authlib.django.client import OAuth
from loginpass import create_django_urlpatterns
from loginpass import Twitter, GitHub, Google

oauth = OAuth()
backends = [Twitter, GitHub, Google]


def handle_authorize(request, remote, token, user_info):
    return JsonResponse(user_info)


urlpatterns = []
for backend in backends:
    oauth_urls = create_django_urlpatterns(backend, oauth, handle_authorize)
    urlpatterns.append(path(backend.NAME + '/', include(oauth_urls)))


def home(request):
    tpl = '<li><a href="/{}/login">{}</a></li>'
    lis = [tpl.format(b.NAME, b.NAME) for b in backends]
    html = '<ul>{}</ul>'.format(''.join(lis))
    return HttpResponse(html)
