from .cart import Cart


# cart context processor
def cart(request):

    # return the default data from the cart
    return {'cart': Cart(request)}
