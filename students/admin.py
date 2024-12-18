from django.contrib import admin
from .models import Department, Course, Semester, Student, Enrollment, Exam, Result

# Register all models
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Student)
admin.site.register(Enrollment)
admin.site.register(Exam)
admin.site.register(Result)
