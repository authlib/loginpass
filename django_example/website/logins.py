from django.http import HttpResponse, JsonResponse
from django.urls import include, path
from authlib.django.client import OAuth
from loginpass import create_django_urlpatterns
from loginpass import (
    Google, Twitter, Facebook, GitHub, Dropbox,
    Reddit, Gitlab, Slack, Discord, StackOverflow,
    Bitbucket
)

OAUTH_BACKENDS = [
    Twitter, Facebook, Google, GitHub, Dropbox,
    Reddit, Gitlab, Slack, Discord, StackOverflow,
    Bitbucket,
]

oauth = OAuth()


def handle_authorize(request, remote, token, user_info):
    return JsonResponse(user_info)


urlpatterns = []
for backend in OAUTH_BACKENDS:
    oauth_urls = create_django_urlpatterns(backend, oauth, handle_authorize)
    urlpatterns.append(path(backend.OAUTH_NAME + '/', include(oauth_urls)))


def home(request):
    tpl = '<li><a href="/{}/login">{}</a></li>'
    lis = [tpl.format(b.OAUTH_NAME, b.OAUTH_NAME) for b in OAUTH_BACKENDS]
    html = '<ul>{}</ul>'.format(''.join(lis))
    return HttpResponse(html)
