from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def send_approval_email(sender, instance, **kwargs):
    if instance.is_active and not instance.last_login:
        send_mail(
            subject='Your account has been approved!',
            message=f'Hello {instance.username}, your account has been approved by admin. You can now log in.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=True
        )
