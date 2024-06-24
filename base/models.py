from django.db import models

# Create your models here.

class Sale(models.Model):
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=10,blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} created on {self.createdAt}"