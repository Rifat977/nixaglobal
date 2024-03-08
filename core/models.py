from django.db import models
from django.contrib.auth import get_user_model

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

    def __str__(self):
        return f"Commission Tier for {self.user.username} at {self.university.name}"