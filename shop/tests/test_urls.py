from django.test import TestCase
from django.test import Client


class UrlTest(TestCase):

    # Using client instance
    def test_RootPage_GET(self):
        response = self.client.get('/', {}, True)
        print(response)

        self.assertEqual(response.status_code, 200)

    # Using client instance
    def test_HomePage_GET(self):
        response = self.client.get('/home', {}, True)
        print(response)

        self.assertEqual(response.status_code, 200)

    # Using client instance
    def test_SearchPage_GET(self):
        response = self.client.get('/search', {}, True)
        print(response)

        self.assertEqual(response.status_code, 200)

    # Using client instance
    def test_SearchPage_POST(self):
        self.csrf_client = Client(enforce_csrf_checks=True)
        response = self.csrf_client.post('/search', params={"item_name": "product"}, follow=True)
        print(response)

        self.assertEqual(response.status_code, 200)

    # Using client instance
    def test_ProductsPage_GET(self):
        response = self.client.get('/products', {}, True)
        print(response)

        self.assertEqual(response.status_code, 200)

    # Product detail

    # Using client instance
    def test_AboutPage_GET(self):
        response = self.client.get('/about', {}, True)
        print(response)

        self.assertEqual(response.status_code, 200)

    # Using client instance
    def test_ContactPage_GET(self):
        response = self.client.get('/contact', {}, True)
        print(response)

        self.assertEqual(response.status_code, 200)

    # Using client instance
    def test_ContactPage_POST(self):
        self.csrf_client = Client(enforce_csrf_checks=True)
        response = self.csrf_client.post('/contact',
                                         params={
                                             "name": "Petr Havlíček",
                                             "email": "havlicekdev@seznam.cz",
                                             "message": "This is ContactPage_POST unit test!"},
                                         follow=True
                                         )
        print(response)

        self.assertEqual(response.status_code, 200)

    # Using client instance
    def test_CartPage_GET(self):
        response = self.client.get('/cart', {}, True)
        print(response)

        self.assertEqual(response.status_code, 200)

    # Using client instance
    def test_CartRemoveItemPage_POST(self):
        self.csrf_client = Client(enforce_csrf_checks=False)
        response = self.csrf_client.post('/cart/remove-item', params={"remove_item_id": "1"}, follow=True)
        print(response)

        self.assertEqual(response.status_code, 200)

    # Using client instance
    def test_CheckoutPage_GET(self):
        response = self.client.get('/checkout', {}, True)
        print(response)

        self.assertEqual(response.status_code, 200)

    # Using client instance
    def test_CheckoutPage_POST(self):
        self.csrf_client = Client(enforce_csrf_checks=True)
        response = self.csrf_client.post('/checkout', params={}, follow=True)
        print(response)

        self.assertEqual(response.status_code, 200)
