
from rest_framework.test import APITestCase, APIClient
from .test_utils import bootstrap_rbac, create_user

class ProfileTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        bootstrap_rbac()


    def setUp(self):
        self.client = APIClient()


    def test_patch_profile(self):
        create_user("u@example.com","Uu123456!","U")
        res = self.client.post("/api/auth/login/", {"email":"u@example.com","password":"Uu123456!"}, format="json")
        access = res.data["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        p = self.client.patch("/api/auth/profile/", {"first_name":"Updated"}, format="json")
        self.assertEqual(p.status_code, 200)
        self.assertEqual(p.data["first_name"], "Updated")


    def test_soft_delete_user(self):
        create_user("d@example.com","Dd123456!","Del")
        res = self.client.post("/api/auth/login/", {"email":"d@example.com","password":"Dd123456!"}, format="json")
        access = res.data["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        r = self.client.delete("/api/auth/profile/")
        self.assertEqual(r.status_code, 200)

        profile = self.client.get("/api/auth/profile/")
        self.assertEqual(profile.status_code, 401)
