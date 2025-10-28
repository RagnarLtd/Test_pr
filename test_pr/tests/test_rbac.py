
from rest_framework.test import APITestCase, APIClient
from .test_utils import bootstrap_rbac, create_user
from access.models import UserRole

class RBACTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_role, cls.manager_role, cls.viewer_role = bootstrap_rbac()


    def setUp(self):
        self.client = APIClient()


    def login(self, email, password):
        res = self.client.post("/api/auth/login/", {"email":email, "password":password}, format="json")
        self.assertEqual(res.status_code, 200, res.content)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access_token']}")


    def test_admin_sees_all(self):
        u = create_user("admin@example.com","Admin1234!","Admin")
        UserRole.objects.get_or_create(user=u, role=self.admin_role)
        self.login("admin@example.com","Admin1234!")

        pr = self.client.get("/api/resources/projects/")
        dc = self.client.get("/api/resources/documents/")
        self.assertEqual(pr.status_code, 200)
        self.assertEqual(dc.status_code, 200)
        self.assertGreaterEqual(len(pr.data), 2)
        self.assertGreaterEqual(len(dc.data), 2)


    def test_viewer_forbidden_projects_but_can_documents_any(self):
        u = create_user("testuser2@example.com","testuser2!","Bob")
        UserRole.objects.get_or_create(user=u, role=self.viewer_role)
        self.login("testuser2@example.com","testuser2!")

        pr = self.client.get("/api/resources/projects/")
        self.assertEqual(pr.status_code, 403)

        dc = self.client.get("/api/resources/documents/")
        self.assertEqual(dc.status_code, 200)
        self.assertGreaterEqual(len(dc.data), 2)
