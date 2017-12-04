from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
# Create your tests here.

class LoginTestCase(TestCase):

    def setUp(self):
        class_user = get_user_model()
        user = class_user()
        user.first_name = "Teste"
        user.email = "test@test.com"
        user.set_password("test1234")
        user.save()
        self.client = Client()

    def test_login(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("login"), {"email" : "test@test.com", "password" : "test1234"} )
        self.assertRedirects(response, "/users/view/")

    def test_login_error(self):
        response = self.client.post(reverse("login"), {"email" : "test@test.com", "password" : "test12345"} )
        self.assertContains(response, u'Senha ou email inválidos')


class RegisterTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register(self):
        response = self.client.get(reverse("register_student"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("register_student"), {"name": "Gustavo Pereira", "email" : "test@test.com","phone" : "987654312", "password" : "test1234", "password_confirm" : "test1234" } )
        self.assertContains(response, u'Usuário criado com sucesso.')

    def test_login_error(self):
        response = self.client.post(reverse("login"), {"email" : "test@test.com", "password" : "test12345"} )
        self.assertContains(response, u'Senha ou email inválidos')
