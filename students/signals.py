import logging
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver, Signal
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import Student, Enrollment, Result, Exam

# Configure the logger
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    """Automatically create a Student profile when a new User is created."""
    if created:
        Student.objects.create(user=instance, name=instance.username)
        print(f"Student profile created for User: {instance.username}")

@receiver(pre_save, sender=Result)
def validate_marks(sender, instance, **kwargs):
    """Ensure marks_obtained does not exceed max_marks."""
    if instance.marks_obtained > instance.max_marks:
        print(f"Invalid marks detected for Result: {instance}. Marks obtained ({instance.marks_obtained}) exceeds maximum ({instance.max_marks}).")
        raise ValueError("Marks obtained cannot exceed maximum marks.")
    logger.info(f"Result validated for Student: {instance.student.name}, Exam: {instance.exam.name}")

@receiver(post_delete, sender=Student)
def delete_related_enrollments(sender, instance, **kwargs):
    """Automatically delete all enrollments of a student when the student is deleted."""
    print(f"Deleting all enrollments for Student: {instance.name}")
    instance.enrollment_set.all().delete()

# Custom Signal
exam_created_signal = Signal()

@receiver(exam_created_signal)
def notify_students_about_exam(sender, instance, **kwargs):
    """Notify students in the course when an exam is created."""
    course = instance.course
    students = Student.objects.filter(enrollment__course=course).distinct()
    for student in students:
        print(f"Notification sent to Student: {student.name} for Exam: {instance.name}, Course: {course.name}")
    print(f"Exam notification sent for Exam: {instance.name}, Course: {course.name}")

@receiver(post_save, sender=Exam)
def trigger_exam_notification(sender, instance, created, **kwargs):
    """Trigger custom signal when a new exam is created."""
    if created:
        print(f"Exam created: {instance.name}, Course: {instance.course.name}")
        exam_created_signal.send(sender=Exam, instance=instance)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log user login events."""
    print(f"User logged in: {user.username} from IP: {request.META.get('REMOTE_ADDR')}")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Log user logout events."""
    print(f"User logged out: {user.username} from IP: {request.META.get('REMOTE_ADDR')}")
