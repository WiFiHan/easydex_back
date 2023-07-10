from django.urls import path
from .views import DexUserView
app_name = 'dexmanager'
urlpatterns = [
    # FBV url path
    path("dexmanager/", DexUserView, name='get'),
]