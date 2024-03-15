from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class CommissionTier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    foundation_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    diploma_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bachelor_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    masters_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    phd_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    research_based_commission = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Commission Tier for {self.user.username} at {self.university.name}"


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    passport_number = models.CharField(max_length=20)
    dob = models.DateField()
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    program = models.CharField(max_length=20, choices=[
        ('FOUNDATION', 'Foundation'),
        ('DIPLOMA', 'Diploma'),
        ('BACHELOR', 'Bachelor'),
        ('MASTER', 'Master'),
        ('PHD', 'PhD'),
    ])
    application_id = models.CharField(max_length=10, unique=True)
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETE', 'Complete'),
        ('REJECT', 'Reject'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    isPaymentClaim = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ApplicationStatus(models.Model):
    application = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=100)
    remark = models.TextField()

    def __str__(self):
        return f"{self.date} - {self.status}"


class PaymentRequest(models.Model):
    STATUS_CHOICES = (
        ('Claimed', 'Claimed'),
        ('Approved', 'Approved'),
        ('Reject', 'Reject'),
        ('Paid', 'Paid'),
    )

    AGENT_TYPE_CHOICES = (
        ('Local', 'Local'),
        ('Foreign', 'Foreign'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    agreed_commission = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=50)
    comment = models.TextField()

    account_holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)

    country_name = models.CharField(max_length=100)
    payee_address = models.TextField()
    bank_address = models.TextField()
    swift_code = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=50, blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.status}"
