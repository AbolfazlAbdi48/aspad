from django.conf import settings
from shop_module.models import Product


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save user cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart.
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = item['price']
            item['total_price'] = item['price'] * item['count']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['count'] for item in self.cart.values())

    def save(self):
        # make the session as "modified" to make sure it gets saved.
        self.session.modified = True

    def add(self, product, count=1, override_count=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'count': 0,
                'price': product.price
            }

        if override_count:
            self.cart[product_id]['count'] = count
        else:
            self.cart[product_id]['count'] += count
        self.save()

    def remove(self, product):
        product_id = product.id
        if str(product_id) in self.cart:
            del self.cart[str(product_id)]
            self.save()

    def clear(self):
        """
        Remove cart from session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(item['price'] * item['count'] for item in self.cart.values())
