from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart
from .forms import CartForm


def cart_page(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartForm(
            initial={'quantity': item['quantity'], 'updated': True})
    return render(request, 'cart/cart.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    form = CartForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data.get("quantity")
        updated = form.cleaned_data.get("updated")

        cart.add(product=product, quantity=quantity, updated_quantity=updated)

    return redirect("cart:cart_page")


@require_POST
def delete_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)

    cart.remove(product=product)
    return redirect("cart:cart_page")
