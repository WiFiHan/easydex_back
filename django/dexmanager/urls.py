from django.urls import path
from .views import DexListView, DexDetailView, UserDexView, EcoDexView, HankyungView
app_name = 'dexmanager'
urlpatterns = [
    # FBV url path
    path("", DexListView.as_view()),
    path("<int:dex_id>/", DexDetailView.as_view()),
    path("economy/", EcoDexView.as_view()),
    path("hankyung/", HankyungView.as_view()),
    path("<int:dex_id>/userdex/", UserDexView.as_view()),
]