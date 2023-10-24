from django.shortcuts import render
from collections import defaultdict
from accounts.models import User, Family
from base.models import Expense
from django.db.models import Q

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
    user_family = None
    if request.user.is_authenticated:
        user = request.user
        user_family = Family.objects.filter(
            Q(parents=user) | Q(kids=user)
        ).first()

        user_expenses = Expense.objects.filter(user=user)
        expenses_distribution = {}
        activities_track = {}
        for expense in user_expenses:
            year = expense.date.year
            month = expense.date.month
            day = expense.date.day
            if year not in expenses_distribution:
                expenses_distribution[year] = {}
                activities_track[year] = {}
            if month not in expenses_distribution[year]:
                expenses_distribution[year][month] = {}
                activities_track[year][month] = {}
            if day not in expenses_distribution[year][month]:
                expenses_distribution[year][month][day] = int(expense.price)
                activities_track[year][month][day] = 1
            else:
                expenses_distribution[year][month][day] += int(expense.price)
                activities_track[year][month][day] += 1
    
    context = {
        "sidebar_menu": sidebar_menu,
        "user": user,
        "user_family": user_family,
        "expenses_distribution": expenses_distribution,
        "activities_track": activities_track,
    }

    return render(request, 'base/home.html', context)
