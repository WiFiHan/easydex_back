from django.urls import path
from .views import DexListView, DexDetailView, UserDexView
app_name = 'dexmanager'
urlpatterns = [
    # FBV url path
    path("dexlist/", DexListView.as_view()),
    path("dexmanager/", UserDexView.as_view(), name='get'),
]