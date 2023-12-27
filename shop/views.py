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
class Root(View):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.response = None

    def get(self, request):
        self.response = redirect('index')
        return self.response


# searching products
"""
def search(request):
    the_cart = Cart(request)
    cart_quantity = the_cart.get_quantity()

    found_objects = None
    item_name = None

    if request.method == "POST":
        item_name = request.POST.get('item_name')

        if item_name != '' and item_name is not None:
            found_objects = Product.objects.filter(title__icontains=item_name)

        else:
            item_name = "Nebyl zadán žádný vyhledávaný text!"

    return render(
        request,
        'shop/search.html',
        {
            'found_objects': found_objects,
            'item_name': item_name,
            'cart_quantity': cart_quantity
        })

"""


class Search(View):

    def __init__(self, **kwargs):
        super().__init__(kwargs)
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
def index(request):
    the_cart = Cart(request)
    cart_quantity = the_cart.get_quantity()

    product_objects = Product.objects.all()

    # pagination code
    paginator = Paginator(product_objects, 10)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)

    return render(
        request,
        'shop/index.html',
        {
            'product_objects': product_objects,
            'cart_quantity': cart_quantity
        })


# products catalog -> list of products
def products(request):
    the_cart = Cart(request)
    cart_quantity = the_cart.get_quantity()

    product_objects = Product.objects.all()

    # pagination code
    paginator = Paginator(product_objects, 4)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)

    return render(
        request,
        'shop/products.html',
        {
            'product_objects': product_objects,
            'cart_quantity': cart_quantity
        })


# products catalog -> particular product detail
def detail(request, id):
    the_cart = Cart(request)
    cart_quantity = the_cart.get_quantity()

    detail_object = None
    item_id = id

    if item_id != '' and item_id is not None:
        detail_object = Product.objects.get(id=item_id)

    return render(
        request,
        'shop/detail.html',
        {
            'detail_object': detail_object,
            'cart_quantity': cart_quantity
        })


# about us page
def about(request):
    the_cart = Cart(request)
    cart_quantity = the_cart.get_quantity()

    return render(
        request,
        'shop/about.html',
        {
            'cart_quantity': cart_quantity
        })


# contact page
def contact(request):
    # processing the email form
    if request.method == "POST":
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        message = request.POST.get('message', "")

        # form save
        db_message = Message(name=name, email=email, message=message)
        db_message.save()

        # send form data as email
        send_email = Email()
        send_email.send(to_email=email, subject='Kontakt', body=message)

        # success message
        messages.success(request, "Váš email byl odeslán!")

    return render(
        request,
        'shop/contact.html',
        {})


# cart page
def cart(request):
    my_cart = Cart(request)

    cart_products = my_cart.get_products()
    cart_quantity = my_cart.get_quantity()
    cart_total_price = my_cart.get_total_price()

    session_cart = my_cart.get_session_cart()

    return render(request, 'shop/cart.html',
                  {"session_cart": session_cart, "cart_products": cart_products, "cart_quantity": cart_quantity,
                   "cart_total_price": cart_total_price})


# add product into the cart or increment quantity of particular product in the cart - using AJAX
def cart_add(request):
    my_cart = Cart(request)

    # AJAX request
    if (request.POST.get('action')) == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        item_qty = my_cart.add(product=product)
        cart_quantity = my_cart.get_quantity()
        item_price = product.price * item_qty
        total_price = my_cart.get_total_price()

        response = JsonResponse(
            {'qty': item_qty, 'item_price': item_price, 'total_price': total_price, "cart_quantity": cart_quantity})
        return response


# decrement quantity of particular item in the cart using AJAX
def cart_dec(request):
    my_cart = Cart(request)

    # AJAX request
    if (request.POST.get('action')) == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        item_qty = my_cart.dec(product=product)
        cart_quantity = my_cart.get_quantity()
        item_price = product.price * item_qty
        total_price = my_cart.get_total_price()

        response = JsonResponse(
            {'qty': item_qty, 'item_price': item_price, 'total_price': total_price, "cart_quantity": cart_quantity})
        return response


# delete all products prom the cart using AJAX
def cart_delete(request):
    my_cart = Cart(request)

    # AJAX request
    if (request.POST.get('action')) == 'post':
        my_cart.delete(request)
        response = JsonResponse({'qty': 0})
        return response


# delete particular product from the cart
def cart_remove_item(request):
    if request.method == "POST":
        my_id = request.POST.get('remove-item-id', "")

        # delete particular item from cart
        my_cart = Cart(request)
        my_cart.remove_cart_item(request, my_id)

    response = redirect('cart')
    return response


# shop checkout
def checkout(request):
    the_user_logged_in = "logged_out"

    the_cart = Cart(request)
    the_checkout = Checkout(request)

    # check if user is logged-in (only logged-in user can make new order)
    if request.user.is_authenticated:
        the_user_logged_in = "logged_in"
        the_user = request.user
        the_user_id = the_user.id

        the_session_cart = the_checkout.get_session_cart()
        the_checkout.set_order()

        total_order_price = the_cart.get_total_price()

        # set up the email message - conformation of order
        message = "Dobrý den,\nděkujeme za Vaši objednávku.\n\n"
        checkout_email_message = the_checkout.get_order_email_confirmation_message()
        for key, value in checkout_email_message.items():
            for key, value in value.items():
                if key == 'product_title':
                    message += "Název produktu: " + str(value) + "\n"

                elif key == 'product_price':
                    message += "Cena/ks: " + str(value) + " Kč\n"

                elif key == 'product_quantity':
                    message += "Počet ks: " + str(value) + "\n"

                elif key == 'product_item_price':
                    message += "Položková cena: " + str(value) + " Kč\n"

                else:
                    pass

            message += "\n\n"
        message += "CELKOVÁ CENA OBJEDNÁVKY: " + str(total_order_price) + " Kč"

        # empty the cart after successfully made new order
        the_checkout.delete_cart(request)

        # email save
        db_message = Message(name=the_user, email=the_user.email, message=message)
        db_message.save()

        # send email
        send_email = Email()
        send_email.send(to_email=the_user.email, subject='Objednávka přijata ke zpracování', body=message)

    else:
        # if user is NOT logged-in -> login
        return redirect('login')

    return render(
        request,
        'shop/checkout.html',
        {

        })
