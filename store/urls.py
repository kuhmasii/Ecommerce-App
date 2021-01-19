from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.store_page, name="store_page"),
    path("<slug:category_slug>/", views.store_page, name="store_page"),
    path("<slug:slug>/<int:detail_id>/",
         views.detail_page, name="detail_page"),
]
