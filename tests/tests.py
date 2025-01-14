from django.test import TestCase
from django.urls import reverse
from snapshottest.django import TestCase as SnapshotTestCase
from students.models import Course, Department
import json


class MyViewTests(TestCase):
    def setUp(self):
       # Create course data in the database
       department = Department.objects.create(id=1, name="Computer Science")  # Create a department with id=1

       # Create course data in the database with valid department_id
       Course.objects.create(id=1, name="OPPS", code="5465", department=department)
       Course.objects.create(id=2, name="Python Programming", code="6764", department=department)
       Course.objects.create(id=3, name="DSA", code="4542", department=department)

    def test_api_response(self):
        # Call the view
        response = self.client.get(reverse('course-list'))
        print(response.content)

        # Check HTTP status
        self.assertEqual(response.status_code, 200)

        # Load the expected data from the JSON file
        with open('tests/expected_output/course_list_expected.json', 'r') as f:
            expected_data = json.load(f)

        # Compare the actual and expected response data
        self.assertEqual(response.json(), expected_data)

class MyViewTestsSnap(SnapshotTestCase):
    def setUp(self):
       # Create course data in the database
       department = Department.objects.create(id=1, name="Computer Science")  # Create a department with id=1

       # Create course data in the database with valid department_id
       Course.objects.create(id=1, name="OPPS", code="5465", department=department)
       Course.objects.create(id=2, name="Python Programming", code="6764", department=department)
       Course.objects.create(id=3, name="DSA", code="4542", department=department)
    def test_api_response_matches_snapshot(self):
        # Send a test request to your view
        response = self.client.get(reverse('course-list'))
        print(response.content)
        # Assert the response matches the snapshot
        self.assertMatchSnapshot(response.json())

# from snapshottest import TestCase
# from students.models import Department, Course
# from django.urls import reverse
# import snapshottest
# from unittest.mock import patch
# from django.contrib.auth.models import User
#
#
# class CourseMockSnapshotTestCase(TestCase):
#     def setUp(self):
#         # Create a sample department for testing
#         self.department = Department.objects.create(name="Computer Science")
#
#         # Create a user for basic authentication
#         self.user = User.objects.create_user(
#             username="testuser", password="password123"
#         )
#
#         # URL for the course API
#         self.course_url = reverse("course-list")  # Adjust based on your route name
#
#         # Create some courses for GET testing
#         self.course1 = Course.objects.create(
#             name="Python Programming", code="ITA0043", department=self.department
#         )
#         self.course2 = Course.objects.create(
#             name="Data Structures", code="ITA0044", department=self.department
#         )
#
#     def test_post_course_with_mock(self):
#         # Mocking the `Course.objects.create` method
#         with patch("students.models.Course.objects.create") as mock_create:
#             # Sample data for creating a course
#             data = {
#                 "name": "Machine Learning",
#                 "code": "ITA0050",
#                 "department": self.department.id,
#             }
#
#             # Mock the return value of `create`
#             mock_create.return_value = Course(
#                 id=3, name=data["name"], code=data["code"], department=self.department
#             )
#
#             # Authenticate the user using Basic Authentication
#             self.client.login(username="testuser", password="password123")
#
#             # Perform POST request
#             response = self.client.post(self.course_url, data, format="json")
#             # Assert the response status
#             self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#             mock_create.assert_called_once_with(
#                 name=data["name"], code=data["code"], department=self.department
#             )
#
#     def test_get_course_list_with_mock(self):
#         # Mocking the `Course.objects.all` method
#         with patch("students.models.Course.objects.all") as mock_all:
#             # Define mocked courses data
#             mock_all.return_value = [
#                 Course(
#                     id=1,
#                     name="Python Programming",
#                     code="ITA0043",
#                     department=self.department,
#                 ),
#                 Course(
#                     id=2,
#                     name="Data Structures",
#                     code="ITA0044",
#                     department=self.department,
#                 ),
#             ]
#
#             # Authenticate the user using Basic Authentication
#             self.client.login(username="testuser", password="password123")
#
#             # Perform GET request
#             response = self.client.get(self.course_url, format="json")
#
#             # Assert the response status
#             self.assertEqual(response.status_code, status.HTTP_200_OK)

