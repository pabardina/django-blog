from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url('^$', 'blog.views.list_articles', name="blog_article_index"),
    url('^(?P<slug>[-\w]+)/$', 'blog.views.article',
        name="blog_article_single"),
    url(r'^like/(\d+)/$', 'blog.views.like', name='like'),
    url(r'^cv.html$', TemplateView.as_view(template_name='cv.html'), name="cv"),
)
