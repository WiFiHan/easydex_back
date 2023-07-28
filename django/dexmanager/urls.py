from django.urls import path
from .views import DexListView, DexDetailView, UserDexView, EcoDexView, HankyungView
app_name = 'dexmanager'
urlpatterns = [
    # FBV url path
    path("", DexListView.as_view()),
    path("values/", DexDetailView.as_view()),
    path("userdex/", UserDexView.as_view()),
    path("economy/", EcoDexView.as_view()),
    path("hankyung/", HankyungView.as_view()),
]