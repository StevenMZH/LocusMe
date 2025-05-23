from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title="Eulerian Hades APIs")),
    
    # APIs
    path('users/', include('users.urls')),
    path('', include('devices.urls')),
            
    # allAuth Authentication
    # path('auth/', include('dj_rest_auth.urls')),
    # path('accounts/', include('allauth.urls')),
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('auth/social/', include('allauth.socialaccount.urls')),
]
