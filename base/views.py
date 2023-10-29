from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from collections import defaultdict
from accounts.models import User, Family
from base.models import Expense
from shops.models import Product, Receipt
from django.db.models import Q, Sum
from django.utils import timezone

@login_required
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
    popular_topics_list = None
    recent_receipt = None
    activities_track = None
    all_user_receipts = None
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
        
        current_month = timezone.now().month  
        current_month_expenses = user_expenses.filter(date__month=current_month)
        popular_topics = current_month_expenses.values('type__name').annotate(total_spent=Sum('price')).order_by('-total_spent')[:3]
        popular_topics_list = [
            {
            'topic': topic['type__name'],  
            'amountSpent': topic['total_spent']  
            } for topic in popular_topics
        ]

        for receipt in user.all_user_receipts:
            receipt.reduce_receipt_products()
        all_user_receipts = user.all_user_receipts

        recent_receipt = Receipt.objects.filter(user=user).order_by('-date').first()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
                if product in user.favorite_products.all():
                    user.favorite_products.remove(product)
                else:
                    user.favorite_products.add(product)
                return HttpResponseRedirect(reverse('base:home'))
            except Product.DoesNotExist:
                pass

    context = {
        "sidebar_menu": sidebar_menu,
        "user": user,
        "user_family": user_family,
        "expenses_distribution": expenses_distribution,
        "activities_track": activities_track,
        "popular_topics_list": popular_topics_list,
        "recent_receipt": recent_receipt,
        "all_user_receipts": all_user_receipts,
    }

    return render(request, 'base/home.html', context)
