
from rest_framework.test import APITestCase, APIClient
from accounts.models import User
from access.models import RevokedToken
from .test_utils import bootstrap_rbac, create_user

class AuthFlowTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        bootstrap_rbac()


    def setUp(self):
        self.client = APIClient()


    def test_register_and_login(self):
        payload = {
            "email": "newuser@example.com",
            "password": "NewUser123!",
            "password2": "NewUser123!",
            "first_name": "New",
            "last_name": "User"
        }
        res = self.client.post("/api/auth/register/", payload, format="json")
        self.assertEqual(res.status_code, 200, res.content)

        res = self.client.post("/api/auth/login/", {"email":"newuser@example.com","password":"NewUser123!"}, format="json")
        self.assertEqual(res.status_code, 200, res.content)
        access = res.data["access_token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        me = self.client.get("/api/auth/profile/")
        self.assertEqual(me.status_code, 200, me.content)
        self.assertEqual(me.data["email"], "newuser@example.com")


    def test_login_invalid_password(self):
        create_user("a@example.com","Aa123456!")
        res = self.client.post("/api/auth/login/", {"email":"a@example.com","password":"wrong"}, format="json")
        self.assertEqual(res.status_code, 401)


    def test_logout_blacklists_token(self):
        create_user("b@example.com","Bb123456!")
        res = self.client.post("/api/auth/login/", {"email":"b@example.com","password":"Bb123456!"}, format="json")
        access = res.data["access_token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        out = self.client.post("/api/auth/logout/")
        self.assertEqual(out.status_code, 200)

        self.assertTrue(RevokedToken.objects.exists())

        again = self.client.get("/api/auth/profile/")
        self.assertEqual(again.status_code, 401)
