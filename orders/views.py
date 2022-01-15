from django.shortcuts import render, redirect
from django.urls import  reverse
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
            # set the order in the session
            print("before session", request.session)
            request.session['order_id'] = order.id
            print(request.session)
            #redirect for payment
            # return render(request, 'orders/success_page.html', dict(order=order))
            return redirect(reverse('payment:payment_process'))
    else:
        form = OrderForm()

    return render(request, "orders/checkout-page.html", dict(form=form, cart=cart))
