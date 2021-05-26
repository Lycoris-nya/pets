from django.urls import path
from .views import PetView, PhotoView

app_name = "pets"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('pets', PetView.as_view()),
    path('pets/<str:pk>/photo', PhotoView.as_view())
]
