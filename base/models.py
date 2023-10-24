from django.db import models
from accounts.models import User

class Expense_type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.CharField(max_length=200, blank=True)
    type = models.ForeignKey(Expense_type, on_delete=models.SET_NULL, null=True, blank=True)
    is_receipt = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.description:
            return f"{self.user.first_name} {self.user.last_name} | {self.date} | {self.description}"
        elif self.type:
            return f"{self.user.first_name} {self.user.last_name} | {self.date} | {self.type}"
        else:
            return f"{self.user.first_name} {self.user.last_name} | {self.date}"
