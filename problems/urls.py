from django.conf.urls import url

from problems.views import HomeView, ProblemView, SolutionView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^problem/(?P<name_slug>[\w-]+)/$', ProblemView.as_view(), name='problem'),
    url(r'^solution/(?P<name_slug>[\w-]+)/$', SolutionView.as_view(), name='solution'),
]
