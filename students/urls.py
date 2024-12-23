from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("departments", DepartmentViewSet)
router.register("courses", CourseViewSet)
router.register("semesters", SemesterViewSet)
router.register("students", StudentViewSet)
router.register("enrollments", EnrollmentViewSet)
router.register("exams", ExamViewSet)
router.register("results", ResultViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
