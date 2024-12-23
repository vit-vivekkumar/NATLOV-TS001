import logging
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver, Signal
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import Student, Enrollment, Result, Exam
from slackMessage.views import send_slack_message

# Configure the logger
logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Result)
def validate_marks(sender, instance, **kwargs):
    """Ensure marks_obtained does not exceed max_marks."""
    if instance.marks_obtained > instance.max_marks:
        error_message = (
            f"Invalid marks detected for Result: {instance}. "
            f"Marks obtained ({instance.marks_obtained}) exceed maximum ({instance.max_marks})."
        )
        send_slack_message(
            user_id=instance.student.user.id,
            effect="Validation Error",
            message=error_message,
        )
        logger.error(error_message)
        raise ValueError("Marks obtained cannot exceed maximum marks.")
    success_message = (
        f"Result validated for Student: {instance.student.name}, "
        f"Exam: {instance.exam.name}, Marks: {instance.marks_obtained}/{instance.max_marks}"
    )
    send_slack_message(
        user_id=instance.student.user.id,
        effect="Validation Success",
        message=success_message,
    )
    logger.info(success_message)


@receiver(post_delete, sender=Student)
def delete_related_enrollments(sender, instance, **kwargs):
    """Automatically delete all enrollments of a student when the student is deleted."""
    message = (
        f"Deleting all enrollments for Student: {instance.name} (ID: {instance.id})"
    )
    send_slack_message(user_id=instance.id, effect="Student Deletion", message=message)
    logger.info(message)
    instance.enrollment_set.all().delete()


# Custom Signal
exam_created_signal = Signal()


@receiver(exam_created_signal)
def notify_students_about_exam(sender, instance, **kwargs):
    """Notify students in the course when an exam is created."""
    course = instance.course
    students = Student.objects.filter(enrollment__course=course).distinct()
    for student in students:
        message = (
            f"Notification sent to Student: {student.name} (ID: {student.id}) "
            f"for Exam: {instance.name}, Course: {course.name}"
        )
        send_slack_message(
            user_id=student.id, effect="Exam Notification", message=message
        )
        logger.info(message)
    exam_message = (
        f"Exam notification sent for Exam: {instance.name}, Course: {course.name}"
    )
    send_slack_message(user_id=None, effect="Exam Notification", message=exam_message)
    logger.info(exam_message)


@receiver(post_save, sender=Exam)
def trigger_exam_notification(sender, instance, created, **kwargs):
    """Trigger custom signal when a new exam is created."""
    if created:
        message = f"Exam created: {instance.name}, Course: {instance.course.name}"
        send_slack_message(user_id=None, effect="Exam Creation", message=message)
        logger.info(message)
        exam_created_signal.send(sender=Exam, instance=instance)
