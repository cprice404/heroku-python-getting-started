from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    # url(r'^db', hello.views.db, name='db'),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^nation_login$', hello.views.nation_login, name='nation_login'),
    url(r'^oauth_callback$', hello.views.oauth_callback, name='oauth_callback'),
    url(r'^tags$', hello.views.tags, name='tags'),
    url(r'^replace_tag$', hello.views.replace_tag, name='replace_tag'),
    url(r'^formset$', hello.views.formset, name='formset')
]
