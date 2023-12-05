from django.dispatch import receiver
from django.db.models.signals import post_save
from user.models import OTP
from user.tasks import send_otp_mail


@receiver(post_save, sender=OTP)
def after_otp(sender: OTP, instance : OTP, **kwargs):
    if not kwargs.get('created', False): return
    
    message = f"Hello, this is your otp {instance.otp}, please don't share it with others."
    
    send_otp_mail(instance.object, message,mail_subject="Password Reset")
    
    # if using celery use :    send_otp_mail.delay(instance.object, message,mail_subject="Password Reset")
