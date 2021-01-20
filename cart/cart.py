from django.conf import settings
from store.models import Product
from decimal import Decimal


class Cart:
    def __init__(self, request):
        """
        getting or
        Initializing a
        session for our cart

        """

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterating over items in cart and
        getting them from the database.

        """
        product_ids = self.cart.keys()

        # getting the product object and adding them to cart.
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product

        for items in cart.values():
            items['price'] = Decimal(items['price'])
            items["total_price"] = items['price'] * items['quantity']
            yield items

    def __len__(self):
        """
        count all items in cart

        """
        return sum(items["quantity"] for items in self.cart.values())

    def add(self, product, quantity=1, updated_quantity=False):
        """
        updating or adding items to the cart

        """

        product_id = str(product.id)
        if not product_id in self.cart:
            self.cart[product_id] = {
                "quantity": 0, "price": str(product.price)}

        if updated_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            if not self.cart[product_id]["quantity"]:
                del self.cart[product_id]
                self.save()
            else:
                self.cart[product_id]['quantity'] -= 1
                self.save()
                if self.cart[product_id]['quantity'] == 0:
                    del self.cart[product_id]
                    self.save()

    def get_total_price(self):
        return sum(Decimal(items['price']) * items['quantity'] for items in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
