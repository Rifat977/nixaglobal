from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class UserType(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    AGENT = 'Agent', 'Agent'
    # SUB_AGENT = 'Sub-agent', 'Sub-agent'
    EXCLUSIVE_AGENT = 'Exclusive Agent', 'Exclusive Agent'

class AccountType(models.TextChoices):
    INDIVIDUAL = 'Individual', 'Individual'
    COMPANY = 'Company', 'Company'

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.AGENT)
    account_type = models.CharField(max_length=20, choices=AccountType.choices, default=AccountType.INDIVIDUAL)
    email = models.EmailField(unique=True) 
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)
    identification_document = models.ForeignKey('IdentificationDocument', on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    profession = models.CharField(max_length=100, null=True, blank=True)

    def is_email_verification_token_expired(self):
        if self.email_verification_sent_at:
            expiration_time = timezone.timedelta(hours=24)  # 24 hours validity
            return self.email_verification_sent_at + expiration_time < timezone.now()
        return True

    @property
    def is_agent(self):
        return self.user_type in [UserType.AGENT]

    @property
    def is_sub_agent(self):
        return self.user_type == UserType.SUB_AGENT

    @property
    def is_admin(self):
        return self.user_type == UserType.ADMIN

    @property
    def is_exclusive_agent(self):
        return self.user_type == UserType.EXCLUSIVE_AGENT

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "     Users"

class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    trade_license = models.FileField(upload_to='user_docs', blank=True, null=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "   Company"

class IdentificationDocument(models.Model):
    DOCUMENT_CHOICES = [
        ('National ID Card', 'National ID Card'),
        ('Birth Certificate', 'Birth Certificate'),
        ('Passport', 'Passport'),
        ('MyKad', 'MyKad'),
        ('iKad', 'iKad'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100, choices=DOCUMENT_CHOICES)

    class Meta:
        verbose_name = "IDENTY Docs"
        verbose_name_plural = "  IDENTY Docs"

class DocumentImage(models.Model):
    identification_document = models.ForeignKey(IdentificationDocument, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_document_images')

    class Meta:
        verbose_name = "Doc Image"
        verbose_name_plural = " Doc Images"

class Referral(models.Model):
    referrer = models.ForeignKey(CustomUser, related_name='referrals_given', on_delete=models.CASCADE)
    referred = models.ForeignKey(CustomUser, related_name='referrals_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Referral"
        verbose_name_plural = "Referrals"
