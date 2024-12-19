from rest_framework.test import APITestCase
from rest_framework import status
from students.models import Department, Course
from django.urls import reverse
import snapshottest
from unittest.mock import patch
from django.contrib.auth.models import User


class CourseMockSnapshotTestCase(APITestCase, snapshottest.TestCase):
    def setUp(self):
        # Create a sample department for testing
        self.department = Department.objects.create(name="Computer Science")

        # Create a user for basic authentication
        self.user = User.objects.create_user(username='testuser', password='password123')

        # URL for the course API
        self.course_url = reverse("course-list")  # Adjust based on your route name

        # Create some courses for GET testing
        self.course1 = Course.objects.create(name="Python Programming", code="ITA0043", department=self.department)
        self.course2 = Course.objects.create(name="Data Structures", code="ITA0044", department=self.department)

    def test_post_course_with_mock(self):
        # Mocking the `Course.objects.create` method
        with patch("students.models.Course.objects.create") as mock_create:
            # Sample data for creating a course
            data = {
                "name": "Machine Learning",
                "code": "ITA0050",
                "department": self.department.id
            }

            # Mock the return value of `create`
            mock_create.return_value = Course(id=3, name=data["name"], code=data["code"], department=self.department)

            # Authenticate the user using Basic Authentication
            self.client.login(username='testuser', password='password123')

            # Perform POST request
            response = self.client.post(self.course_url, data, format="json")

            # Assert the response status
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # Assert that `Course.objects.create` was called once
            mock_create.assert_called_once_with(name=data["name"], code=data["code"], department=self.department)

            # Snapshot the response data
            self.assertMatchSnapshot(response.data)

    def test_get_course_list_with_mock(self):
        # Mocking the `Course.objects.all` method
        with patch("students.models.Course.objects.all") as mock_all:
            # Define mocked courses data
            mock_all.return_value = [
                Course(id=1, name="Python Programming", code="ITA0043", department=self.department),
                Course(id=2, name="Data Structures", code="ITA0044", department=self.department),
            ]

            # Authenticate the user using Basic Authentication
            self.client.login(username='testuser', password='password123')

            # Perform GET request
            response = self.client.get(self.course_url, format="json")

            # Assert the response status
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Snapshot the response data
            self.assertMatchSnapshot(response.data)

            # Ensure that the mocked `Course.objects.all` was called
            mock_all.assert_called_once()
