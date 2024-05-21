from django.urls import path

from . import views

app_name = "deepForest"
urlpatterns = [
    path("", views.main, name="main"),
    path('results/', views.results,
         name='results'),
]
