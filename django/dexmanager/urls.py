from django.urls import path
from .views import DexListView, DexDetailView, UserDexView, EcoDexView
app_name = 'dexmanager'
urlpatterns = [
    # FBV url path
    path("", DexListView.as_view()),
    path("<int:dex_id>/", DexDetailView.as_view()),
    path("userdex/", UserDexView.as_view()),
    path("economy/", EcoDexView.as_view()),
]