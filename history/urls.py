from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from apps.authen.views import Authenticate
from apps.problem.views import Quiz, Result


urlpatterns = patterns('',
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^$', Authenticate.as_view()),
    url(r'^statement/$', login_required(TemplateView.as_view(template_name="statement.html"))),
    url(r'^problems/$', Quiz.as_view()),
    url(r'^achieve/$', Result.as_view()),

    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
)
