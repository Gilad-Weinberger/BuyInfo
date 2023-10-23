from django.shortcuts import render
from collections import defaultdict
from django.contrib.auth.models import User
from .models import Expense

def home(request):
    sidebar_menu = [
        {'text': 'בית', 'link': '/', 'icon': 'fa-regular fa-house', 'alerts_count': 0},
        {'text': 'קבלות', 'link': '/', 'icon': 'fa-regular fa-envelope', 'alerts_count': 0},
        {'text': 'תזכורת', 'link': '/', 'icon': 'fa-regular fa-bell', 'alerts_count': 0},
        {'text': 'ניתוח מידע', 'link': '/', 'icon': 'fa-regular fa-chart-mixed', 'alerts_count': 0},
        {'text': 'הגדרות', 'link': '/', 'icon': 'fa-regular fa-gear', 'alerts_count': 0},
        {'text': 'חשבונות', 'link': '/', 'icon': 'fa-regular fa-circle-user', 'alerts_count': 0},
        {'text': 'עזרה', 'link': '/', 'icon': 'fa-regular fa-circle-info', 'alerts_count': 0},
    ]

    user = None
    expenses_distribution = None
    if request.user.is_authenticated:
        user = request.user

        user_expenses = Expense.objects.filter(user=user)
        expenses_distribution = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        for expense in user_expenses:
            year, month, day = expense.date.year, expense.date.month, expense.date.day
            expenses_distribution[year][month][day] += expense.price

    context = {"sidebar_menu": sidebar_menu, "user": user, "expenses_distribution": expenses_distribution}

    return render(request, 'base/home.html', context)
