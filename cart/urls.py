from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_page, name='cart_page'),
    path("add/<int:product_id>/", views.cart_add, name='cart_add'),
    path("remove/<int:product_id>/", views.delete_cart, name='delete_cart'),
]