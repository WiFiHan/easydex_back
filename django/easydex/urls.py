from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/dexmanager/', include('dexmanager.urls')),
    path('api/account/', include('account.urls')),
]
