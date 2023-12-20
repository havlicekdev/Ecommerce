from shop.models import Product


# cart object
class Cart:

    # init
    def __init__(self, request):

        # variables init
        self.new_cart = None
        self.total_quantity = 0
        self.total_price = 0
        self.product_ids = None

        # session
        self.session = request.session

        # get the current shoppingCart if exists
        self.cart = self.session.get('shoppingCart')

        # if the user is new -> create new shoppingCart
        if 'shoppingCart' not in request.session:
            self.cart = self.session['shoppingCart'] = {}

    # add product into the cart
    def add(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id] = self.cart[product_id] + 1
        else:
            self.cart[product_id] = 1

        self.session.modified = True
        return self.cart[product_id]

    # get cart length
    def __len__(self):
        return len(self.cart)

    # decrement quantity of product item
    def dec(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            if self.cart[product_id] > 1:
                self.cart[product_id] = self.cart[product_id] - 1
            else:
                self.cart[product_id] = 1
        else:
            self.cart[product_id] = 1

        self.session.modified = True
        return self.cart[product_id]

    # get total quantity
    def get_quantity(self):
        for key, value in self.cart.items():
            self.total_quantity += int(value)

        return self.total_quantity

    # get session carts
    def get_session_cart(self):
        return self.cart

    # get products from session cart
    def get_products(self):

        # ids from session cart
        self.product_ids = self.cart.keys()

        # find products in db by id
        products = Product.objects.filter(id__in=self.product_ids)

        return products

    # get total price
    def get_total_price(self):
        # Ids from session cart
        self.product_ids = self.cart.keys()

        # find products in DB by id
        products = Product.objects.filter(id__in=self.product_ids)

        for product in products:
            for key, value in self.cart.items():
                if int(key) == product.id:
                    self.total_price = self.total_price + (int(product.price) * value)

        return self.total_price

    # remove item from the cart
    def remove_cart_item(self, request, my_id):

        self.new_cart = {}

        for key, value in self.session['shoppingCart'].items():
            if int(key) != int(my_id):
                self.new_cart[key] = value

        del request.session['shoppingCart']
        request.session['shoppingCart'] = self.new_cart

        return self.session['shoppingCart']

    # delete all the session cart
    def delete(self, request):
        del request.session['shoppingCart']
