from django.conf.urls import url

from problems.views import HomeView, ProblemView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^problem/(?P<name_slug>[\w-]+)/$', ProblemView.as_view(), name='problem'),
]
