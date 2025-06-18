from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.FloatField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - ₹{self.amount}"

