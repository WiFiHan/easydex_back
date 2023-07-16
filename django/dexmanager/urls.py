from django.urls import path
from .views import DexListView, DexDetailView, UserDexView
app_name = 'dexmanager'
urlpatterns = [
    # FBV url path
    path("", DexListView.as_view()),
    path("/<int:dex_id>/", DexDetailView.as_view()),
    path("/<int:dex_id>/userdex/", UserDexView.as_view()),
]