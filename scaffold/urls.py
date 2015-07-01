from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

import session_csrf
session_csrf.monkeypatch()

from django.contrib import admin
admin.autodiscover()

handler403 = 'blog.views.permission_denied'

urlpatterns = [
    url(r'^$', 'blog.views.index'),
    url( r'^blog/view/(?P<slug>[^\.]+).html', 
        'blog.views.view_post', 
        name='view_blog_post' ),
    url( r'^admin/edit/(?P<slug>[^\.]+).html', 
        'blog.views.edit_post', 
        name='edit_blog_post' ),
    url( r'^admin/delete/(?P<slug>[^\.]+).html', 
        'blog.views.delete_post', 
        name='delete_blog_post' ),
    
    url(r'^admin/add-post', 'blog.views.add_post'),
    url(r'^admin/', 'blog.views.admin'),
    
    url(r'^_ah/', include('djangae.urls')),
    url(r'^djangoadmin/', include(admin.site.urls)),
    url(r'^csp/', include('cspreports.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




