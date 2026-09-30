from django.db import models
from django.contrib.auth.models import User


class Prediction(models.Model):
    customer_name = models.CharField(max_length=100, blank=True)
    contract = models.CharField(max_length=30)
    tenure = models.IntegerField()
    monthly_charges = models.FloatField()
    inputs = models.JSONField()  # all form values
    probability = models.FloatField()
    risk_level = models.CharField(max_length=10)
    action = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def percent(self):
        return round(self.probability * 100, 1)
