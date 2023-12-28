from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .cart import Cart
from .email import Email
from .models import Product, Message
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from shop.checkout import Checkout


# root app entry: redirect to index
class RootView(View):

    # init
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # redirect
    def get(self, request):
        return redirect('index')


# search the product
class SearchView(View):

    # init
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = None
        self.item_name = None
        self.found_objects = None
        self.cart_quantity = None

    # form processing
    def post(self, request):

        # cart quantity for the cart badge
        self.cart = Cart(request)
        self.cart_quantity = self.cart.get_quantity()

        # get found object as QuerySet
        self.item_name = request.POST.get('item_name')
        if self.item_name != '' and self.item_name is not None:
            self.found_objects = Product.objects.filter(title__icontains=self.item_name)

        else:
            self.item_name = "Nebyl zadán žádný vyhledávaný text!"

        # return
        return render(
            request,
            'shop/search.html',
            {
                'found_objects': self.found_objects,
                'item_name': self.item_name,
                'cart_quantity': self.cart_quantity
            })


# home page
class IndexView(View):

    # init
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = None
        self.product_objects = None
        self.page = None
        self.paginator = None
        self.cart_quantity = None

    # get
    def get(self, request):
        # cart quantity for the cart badge
        self.cart = Cart(request)
        self.cart_quantity = self.cart.get_quantity()

        # get all products as QuerySet
        self.product_objects = Product.objects.all()

        # pagination code
        self.paginator = Paginator(self.product_objects, 10)
        self.page = request.GET.get('page')
        self.product_objects = self.paginator.get_page(self.page)

        # return
        return render(
            request,
            'shop/index.html',
            {
                'product_objects': self.product_objects,
                'cart_quantity': self.cart_quantity
            })


# products catalog -> list of products
class ProductsView(View):

    # init
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = None
        self.product_objects = None
        self.page = None
        self.paginator = None
        self.cart_quantity = None

    # get
    def get(self, request):
        # cart quantity for the cart badge
        self.cart = Cart(request)
        self.cart_quantity = self.cart.get_quantity()

        # get all products as QuerySet
        self.product_objects = Product.objects.all()

        # pagination code
        self.paginator = Paginator(self.product_objects, 4)
        self.page = request.GET.get('page')
        self.product_objects = self.paginator.get_page(self.page)

        # return
        return render(
            request,
            'shop/products.html',
            {
                'product_objects': self.product_objects,
                'cart_quantity': self.cart_quantity
            })


# products catalog -> particular product detail
class DetailView(View):

    # init
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = None
        self.item_id = None
        self.cart_quantity = None
        self.detail_object = None

    # get
    def get(self, request, id):
        # cart quantity for the cart badge
        self.cart = Cart(request)
        self.cart_quantity = self.cart.get_quantity()

        # get particular product as QuerySet
        self.item_id = id

        if self.item_id != '' and self.item_id is not None:
            self.detail_object = Product.objects.get(id=self.item_id)

        # return
        return render(
            request,
            'shop/detail.html',
            {
                'detail_object': self.detail_object,
                'cart_quantity': self.cart_quantity
            })


# about us page
class AboutView(View):

    # init
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = None
        self.cart_quantity = None

    # get
    def get(self, request):
        # cart quantity for the cart badge
        self.cart = Cart(request)
        self.cart_quantity = self.cart.get_quantity()

        # return
        return render(
            request,
            'shop/about.html',
            {
                'cart_quantity': self.cart_quantity
            })


# contact page
class ContactView(View):

    # init
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.send_email = None
        self.db_message = None
        self.message = None
        self.email = None
        self.name = None

    # get
    def get(self, request):
        # return
        return render(
            request,
            'shop/contact.html',
            {}
        )

    # post
    def post(self, request):
        # the email form processing
        self.name = request.POST.get('name', "")
        self.email = request.POST.get('email', "")
        self.message = request.POST.get('message', "")

        # form save
        self.db_message = Message(name=self.name, email=self.email, message=self.message)
        self.db_message.save()

        # send form data as email
        self.send_email = Email()
        self.send_email.send(to_email=self.email, subject='Kontakt', body=self.message)

        # success message
        messages.success(request, "Váš email byl odeslán!")

        # return
        return render(
            request,
            'shop/contact.html',
            {}
        )


# cart page
class CartView(View):

    # init
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = None
        self.session_cart = None
        self.cart_total_price = None
        self.cart_quantity = None
        self.cart_products = None

    # get
    def get(self, request):
        # get session cart
        self.session_cart = self.cart.get_session_cart()

        # cart quantity for the cart badge
        self.cart = Cart(request)
        self.cart_quantity = self.cart.get_quantity()

        # get all products in the cart
        self.cart_products = self.cart.get_products()

        # get cart total price
        self.cart_total_price = self.cart.get_total_price()

        # return
        return render(
            request,
            'shop/cart.html',
            {
                "session_cart": self.session_cart,
                "cart_products": self.cart_products,
                "cart_quantity": self.cart_quantity,
                "cart_total_price": self.cart_total_price
            }
        )


# delete all products prom the cart using AJAX
class CartDeleteAjax(View):

    # init
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = None
        self.response = None

    # get
    def post(self, request):
        # AJAX request processing
        self.cart = Cart(request)
        self.cart.delete(request)
        self.response = JsonResponse({'qty': 0})

        # response
        return self.response


# add product into the cart or increment quantity of particular product in the cart - using AJAX
class CartAddAjax(View):

    # init
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_quantity = None
        self.item_qty = None
        self.product = None
        self.product_id = None
        self.my_cart = None

    # post
    def post(self, request):
        self.my_cart = Cart(request)

        # AJAX request processing
        self.product_id = int(request.POST.get('product_id'))
        self.product = get_object_or_404(Product, id=self.product_id)
        self.item_qty = self.my_cart.add(product=self.product)
        self.cart_quantity = self.my_cart.get_quantity()
        item_price = self.product.price * self.item_qty
        total_price = self.my_cart.get_total_price()

        # response
        response = JsonResponse(
            {'qty': self.item_qty, 'item_price': item_price, 'total_price': total_price,
             "cart_quantity": self.cart_quantity})
        return response


# decrement quantity of particular item in the cart using AJAX
class CartDecAjax(View):

    # init
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = None
        self.total_price = None
        self.item_price = None
        self.cart_quantity = None
        self.item_qty = None
        self.product = None
        self.product_id = None

    # post
    def post(self, request):
        self.cart = Cart(request)

        # AJAX request processing
        self.product_id = int(request.POST.get('product_id'))
        self.product = get_object_or_404(Product, id=self.product_id)
        self.item_qty = self.my_cart.dec(product=self.product)
        self.cart_quantity = self.my_cart.get_quantity()
        self.item_price = self.product.price * self.item_qty
        self.total_price = self.my_cart.get_total_price()

        # response
        response = JsonResponse(
            {'qty': self.item_qty, 'item_price': self.item_price, 'total_price': self.total_price,
             "cart_quantity": self.cart_quantity})
        return response


# delete particular product from the cart
class CartRemoveItemView(View):

    # init
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = None
        self.my_id = None

    # post
    def post(self, request):
        # get product id to delete
        self.my_id = request.POST.get('remove-item-id', "")

        # delete particular item from cart
        self.cart = Cart(request)
        self.cart.remove_cart_item(request, self.my_id)

        # response
        response = redirect('cart')
        return response


# shop checkout
class CheckoutView(View):

    # init
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.send_email = None
        self.db_message = None
        self.checkout_email_message = None
        self.message = None
        self.total_order_price = None
        self.session_cart = None
        self.user_id = None
        self.user = None
        self.user_logged_in = None
        self.checkout = None
        self.cart = None

    # post
    def post(self, request):
        self.user_logged_in = "logged_out"
        self.cart = Cart(request)
        self.checkout = Checkout(request)

        # check if user is logged-in (only logged-in user can make new order)
        if request.user.is_authenticated:
            self.user_logged_in = "logged_in"
            self.user = request.user
            self.user_id = self.user.id

            self.session_cart = self.checkout.get_session_cart()
            self.checkout.set_order()

            self.total_order_price = self.cart.get_total_price()

            # set up the email message - conformation of order
            self.message = "Dobrý den,\nděkujeme za Vaši objednávku.\n\n"
            self.checkout_email_message = self.checkout.get_order_email_confirmation_message()

            for key, value in self.checkout_email_message.items():
                for key, value in value.items():
                    if key == 'product_title':
                        self.message += "Název produktu: " + str(value) + "\n"

                    elif key == 'product_price':
                        self.message += "Cena/ks: " + str(value) + " Kč\n"

                    elif key == 'product_quantity':
                        self.message += "Počet ks: " + str(value) + "\n"

                    elif key == 'product_item_price':
                        self.message += "Položková cena: " + str(value) + " Kč\n"

                    else:
                        pass

                self.message += "\n\n"
            self.message += "CELKOVÁ CENA OBJEDNÁVKY: " + str(self.total_order_price) + " Kč"

            # empty the cart after successfully made new order
            self.checkout.delete_cart(request)

            # email save
            self.db_message = Message(name=self.the_user, email=self.the_user.email, message=self.message)
            self.db_message.save()

            # send email
            self.send_email = Email()
            self.send_email.send(to_email=self.the_user.email, subject='Objednávka přijata ke zpracování',
                                 body=self.message)

        else:
            # if user is NOT logged-in -> redirect to login
            return redirect('login')

        # return
        return render(
            request,
            'shop/checkout.html',
            {

            }
        )
