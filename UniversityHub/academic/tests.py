from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class PublicStudentApiTests(TestCase):
    def test_student_list_is_available_without_login(self):
        client = APIClient()
        response = client.get('/academic/api/students/')

        self.assertEqual(response.status_code, 200)
