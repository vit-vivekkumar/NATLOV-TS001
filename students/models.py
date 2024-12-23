import random
from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Semester(models.Model):
    number = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"{self.number} - {self.year}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    enrollment_number = models.CharField(max_length=15, unique=True, auto_created=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.enrollment_number: 
            last_student = Student.objects.all().order_by('id').last()
            if last_student:
                last_number = random.randint(100, 999)
                new_number = last_number + 1
            else:
                new_number = 1 
            self.enrollment_number = f"ITA{new_number:03d}"  # Format as ITA001, ITA002
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.enrollment_number})"
    
    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

class Exam(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    max_marks = models.FloatField()
