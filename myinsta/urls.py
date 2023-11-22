from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts.views import url_view, url_parameter_view, function_view, index
from posts.views import class_view
from posts.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('posts',PostModelViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    # Function Based View
    path('url/', url_view),
    path('accounts/',include('accounts.urls',namespace ='accounts')),
    path('url/<str:username>/', url_parameter_view),
    path('fbv/', function_view),
    # Class Based View
    path('cbv/', class_view.as_view()), # as_view: 진입 메소드

    #path('', index, name='index'),
    #path('',include(router.urls)),
    path('',include('posts.urls')),
    #path('posts/', include('posts.urls', namespace='posts')),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)