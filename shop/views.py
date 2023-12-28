from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .cart import Cart
from .email import Email
from .models import Product, Message
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from shop.checkout import Checkout


# root app entry
class RootView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response = None

    def get(self, request):
        self.response = redirect('index')
        return self.response


# searching products
class SearchView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_name = None
        self.found_objects = None
        self.cart_quantity = None
        self.the_cart = None

    def post(self, request):
        self.the_cart = Cart(request)
        self.cart_quantity = self.the_cart.get_quantity()

        self.item_name = request.POST.get('item_name')
        if self.item_name != '' and self.item_name is not None:
            self.found_objects = Product.objects.filter(title__icontains=self.item_name)

        else:
            self.item_name = "Nebyl zadán žádný vyhledávaný text!"

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_objects = None
        self.page = None
        self.paginator = None
        self.cart_quantity = None
        self.the_cart = None

    def get(self, request):
        self.the_cart = Cart(request)
        self.cart_quantity = self.the_cart.get_quantity()
        self.product_objects = Product.objects.all()

        # pagination code
        self.paginator = Paginator(self.product_objects, 10)
        self.page = request.GET.get('page')
        self.product_objects = self.paginator.get_page(self.page)

        return render(
            request,
            'shop/index.html',
            {
                'product_objects': self.product_objects,
                'cart_quantity': self.cart_quantity
            })


# products catalog -> list of products
class ProductsView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_objects = None
        self.page = None
        self.paginator = None
        self.cart_quantity = None
        self.the_cart = None

    def get(self, request):
        self.the_cart = Cart(request)
        self.cart_quantity = self.the_cart.get_quantity()
        self.product_objects = Product.objects.all()

        # pagination code
        self.paginator = Paginator(self.product_objects, 4)
        self.page = request.GET.get('page')
        self.product_objects = self.paginator.get_page(self.page)

        return render(
            request,
            'shop/products.html',
            {
                'product_objects': self.product_objects,
                'cart_quantity': self.cart_quantity
            })


# products catalog -> particular product detail
class DetailView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_id = None
        self.cart_quantity = None
        self.the_cart = None
        self.detail_object = None

    def get(self, request, id):
        self.the_cart = Cart(request)
        self.cart_quantity = self.the_cart.get_quantity()
        self.item_id = id

        if self.item_id != '' and self.item_id is not None:
            self.detail_object = Product.objects.get(id=self.item_id)

        return render(
            request,
            'shop/detail.html',
            {
                'detail_object': self.detail_object,
                'cart_quantity': self.cart_quantity
            })


# about us page
class AboutView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_quantity = None
        self.the_cart = None

    def get(self, request):
        self.the_cart = Cart(request)
        self.cart_quantity = self.the_cart.get_quantity()

        return render(
            request,
            'shop/about.html',
            {
                'cart_quantity': self.cart_quantity
            })


# contact page
class ContactView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.send_email = None
        self.db_message = None
        self.message = None
        self.email = None
        self.name = None

    def get(self, request):
        return render(
            request,
            'shop/contact.html',
            {}
        )

    def post(self, request):
        # processing the email form
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

        return render(
            request,
            'shop/contact.html',
            {}
        )


# cart page
class CartView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session_cart = None
        self.cart_total_price = None
        self.cart_quantity = None
        self.cart_products = None
        self.my_cart = None

    def get(self, request):
        self.my_cart = Cart(request)
        self.cart_products = self.my_cart.get_products()
        self.cart_quantity = self.my_cart.get_quantity()
        self.cart_total_price = self.my_cart.get_total_price()
        self.session_cart = self.my_cart.get_session_cart()

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response = None
        self.my_cart = None

    def post(self, request):
        # AJAX request
        self.my_cart = Cart(request)
        self.my_cart.delete(request)
        self.response = JsonResponse({'qty': 0})
        return self.response


# add product into the cart or increment quantity of particular product in the cart - using AJAX
class CartAddAjax(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_quantity = None
        self.item_qty = None
        self.product = None
        self.product_id = None
        self.my_cart = None

    def post(self, request):
        self.my_cart = Cart(request)

        # AJAX request
        self.product_id = int(request.POST.get('product_id'))
        self.product = get_object_or_404(Product, id=self.product_id)
        self.item_qty = self.my_cart.add(product=self.product)
        self.cart_quantity = self.my_cart.get_quantity()
        item_price = self.product.price * self.item_qty
        total_price = self.my_cart.get_total_price()

        response = JsonResponse(
            {'qty': self.item_qty, 'item_price': item_price, 'total_price': total_price,
             "cart_quantity": self.cart_quantity})
        return response


# decrement quantity of particular item in the cart using AJAX
class CartDecAjax(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_price = None
        self.item_price = None
        self.cart_quantity = None
        self.item_qty = None
        self.product = None
        self.product_id = None
        self.my_cart = None

    def post(self, request):
        self.my_cart = Cart(request)

        # AJAX request
        self.product_id = int(request.POST.get('product_id'))
        self.product = get_object_or_404(Product, id=self.product_id)
        self.item_qty = self.my_cart.dec(product=self.product)
        self.cart_quantity = self.my_cart.get_quantity()
        self.item_price = self.product.price * self.item_qty
        self.total_price = self.my_cart.get_total_price()

        response = JsonResponse(
            {'qty': self.item_qty, 'item_price': self.item_price, 'total_price': self.total_price,
             "cart_quantity": self.cart_quantity})
        return response


# delete particular product from the cart
class CartRemoveItemView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.my_cart = None
        self.my_id = None

    def post(self, request):
        self.my_id = request.POST.get('remove-item-id', "")

        # delete particular item from cart
        self.my_cart = Cart(request)
        self.my_cart.remove_cart_item(request, self.my_id)

        response = redirect('cart')
        return response


# shop checkout
class CheckoutView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.send_email = None
        self.checkout_email_message = None
        self.message = None
        self.db_message = None
        self.total_order_price = None
        self.the_session_cart = None
        self.the_user_id = None
        self.the_user = None
        self.the_checkout = None
        self.the_cart = None
        self.the_user_logged_in = None

    def post(self, request):
        self.the_user_logged_in = "logged_out"
        self.the_cart = Cart(request)
        self.the_checkout = Checkout(request)

        # check if user is logged-in (only logged-in user can make new order)
        if request.user.is_authenticated:
            self.the_user_logged_in = "logged_in"
            self.the_user = request.user
            self.the_user_id = self.the_user.id

            self.the_session_cart = self.the_checkout.get_session_cart()
            self.the_checkout.set_order()

            self.total_order_price = self.the_cart.get_total_price()

            # set up the email message - conformation of order
            self.message = "Dobrý den,\nděkujeme za Vaši objednávku.\n\n"
            self.checkout_email_message = self.the_checkout.get_order_email_confirmation_message()

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
            self.the_checkout.delete_cart(request)

            # email save
            self.db_message = Message(name=self.the_user, email=self.the_user.email, message=self.message)
            self.db_message.save()

            # send email
            self.send_email = Email()
            self.send_email.send(to_email=self.the_user.email, subject='Objednávka přijata ke zpracování',
                                 body=self.message)

        else:
            # if user is NOT logged-in -> login
            return redirect('login')

        return render(
            request,
            'shop/checkout.html',
            {

            }
        )
