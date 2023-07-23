from django.urls import path
from .views import DexListView, DexDetailView, UserDexView, ECOSopenAPIView
app_name = 'dexmanager'
urlpatterns = [
    # FBV url path
    path("", DexListView.as_view()),
    path("<int:dex_id>/", DexDetailView.as_view()),
    path("userdex/", UserDexView.as_view()),
    path("ecos/", ECOSopenAPIView.as_view())
]