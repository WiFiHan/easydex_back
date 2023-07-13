from django.urls import path
from .views import IndexListView, IndexDetailView

app_name = 'index'
urlpatterns = [
    # FBV url path
    path("", IndexListView.as_view()),
    path("<int:index_id>/", IndexDetailView.as_view()),
]