from django.shortcuts import render

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
    context = {"sidebar_menu": sidebar_menu}

    return render(request, 'base/home.html', context)