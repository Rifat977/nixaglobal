from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from django.core.validators import FileExtensionValidator

User = get_user_model()

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "      University"

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

    class Meta:
        verbose_name = "CommissionTier"
        verbose_name_plural = "       CommissionTier"

    def __str__(self):
        return f"Commission Tier for {self.user.username} at {self.university.name}"

class Subject(models.Model):

    PROGRAM_CHOICES = [
        ('FOUNDATION', 'Foundation'),
        ('DIPLOMA', 'Diploma'),
        ('BACHELOR', 'Bachelor'),
        ('MASTER', 'Master'),
        ('PHD', 'PhD'),
        ("RESEARCH_BASED", 'Research Based')
    ]

    name = models.CharField(max_length=255)
    program_type = models.CharField(max_length=50, choices=PROGRAM_CHOICES)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='subject_pdfs/', validators=[FileExtensionValidator(['pdf'])], blank=True, null=True)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "  Subject"

    def __str__(self):
        return f"{self.name} - {self.program_type}: {self.university}"


class Fee(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Fee"
        verbose_name_plural = " Fee"

    def __str__(self):
        return f"{self.subject} - {self.field_name}: {self.value}"


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    passport_number = models.CharField(max_length=20)
    intake = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    application_id = models.CharField(max_length=10, unique=True)
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETE', 'Complete'),
        ('REJECT', 'Reject'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    isPaymentClaim = models.BooleanField(default=False)


    class Meta:
        verbose_name = "Applicant"
        verbose_name_plural = "      Applicant"



    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ApplicationStatus(models.Model):
    application = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=100)
    remark = models.TextField()

    class Meta:
        verbose_name = "ApplicationStatus"
        verbose_name_plural = "      ApplicationStatus"

    def __str__(self):
        return f"{self.date} - {self.status}"


class PaymentRequest(models.Model):
    STATUS_CHOICES = (
        ('Claimed', 'Claimed'),
        ('Approved', 'Approved'),
        ('Reject', 'Reject'),
        ('Paid', 'Paid'),
    )

    BANK_TYPE_CHOICES = (
        ('Local', 'Local'),
        ('Foreign', 'Foreign'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    agreed_commission = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=50)
    comment = models.TextField()

    bank_type = models.CharField(max_length=10, choices=BANK_TYPE_CHOICES, default='Local')

    account_holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)

    country_name = models.CharField(max_length=100, null=True, blank=True)
    payee_address = models.TextField(null=True, blank=True)
    bank_address = models.TextField(null=True, blank=True)
    swift_code = models.CharField(max_length=50, null=True, blank=True)
    ifsc_code = models.CharField(max_length=50, blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Claimed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "PaymentRequest"
        verbose_name_plural = "   PaymentRequest"

    def __str__(self):
        return f"{self.user} - {self.status}"

