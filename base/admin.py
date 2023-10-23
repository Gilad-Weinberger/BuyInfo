from django.contrib import admin
from .models import Expense, Expense_type

admin.site.register(Expense)
admin.site.register(Expense_type)