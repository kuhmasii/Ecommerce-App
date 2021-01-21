from django.shortcuts import render
from .forms import OrderForm
from .models import OrderItem
from cart.cart import Cart
from .tasks import order_created


def order_page(request):

    cart = Cart(request)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )
            # clear cart
            cart.clear()
            # lauching asynchronous task
            order_created.delay(order.id)
            return render(request, 'orders/success_page.html', dict(order=order))
    else:
        form = OrderForm()

    return render(request, "orders/checkout-page.html", dict(form=form, cart=cart))
