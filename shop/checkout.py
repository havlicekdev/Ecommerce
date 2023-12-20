from datetime import datetime
from shop.cart import Cart
from shop.models import Order, Order_items, Product, Message


# shop checkout
class Checkout:

    # init
    def __init__(self, request):
        self.product_item_price = None
        self.product_quantity = None
        self.product_price = None
        self.order_email_confirmation_message_item = None
        self.order_email_confirmation_message = None
        self.session_cart = None
        self.the_cart = Cart(request)
        self.the_user = request.user

    # get session cart
    def get_session_cart(self):
        return self.the_cart.get_session_cart()

    # set order
    def set_order(self):

        # save order into db
        db_order = Order(user=self.the_user, datetime=datetime.now(), status='PR')
        db_order.save()

        # save order items into db
        self.session_cart = self.the_cart.get_session_cart()

        for key, value in self.session_cart.items():
            db_product = Product.objects.get(id=int(key))

            self.product_price = db_product.price
            self.product_quantity = value
            self.product_item_price = db_product.price * self.product_quantity

            db_order_items = Order_items(
                order=db_order,
                product=db_product,
                product_title=db_product.title,
                product_price=self.product_price,
                product_quantity=self.product_quantity,
                product_item_price=self.product_item_price,
                product_category=db_product.category,
                product_description=db_product.description
            )
            db_order_items.save()

    # delete all the cart
    def delete_cart(self, request):
        self.the_cart.delete(request)

    # get total price of the cart
    def get_total_price(self):
        self.the_cart.get_total_price()

    # get order email confirmation message
    def get_order_email_confirmation_message(self):

        self.order_email_confirmation_message = {}

        self.session_cart = self.the_cart.get_session_cart()

        for key, value in self.session_cart.items():
            self.order_email_confirmation_message_item = {}

            db_product = Product.objects.get(id=int(key))

            self.product_price = db_product.price
            self.product_quantity = value
            self.product_item_price = db_product.price * self.product_quantity

            self.order_email_confirmation_message_item['product_title'] = db_product.title
            self.order_email_confirmation_message_item['product_price'] = self.product_price
            self.order_email_confirmation_message_item['product_quantity'] = self.product_quantity
            self.order_email_confirmation_message_item['product_item_price'] = self.product_item_price

            self.order_email_confirmation_message[key] = self.order_email_confirmation_message_item

        return self.order_email_confirmation_message
