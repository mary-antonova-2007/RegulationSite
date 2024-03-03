from django.shortcuts import render, redirect
from .models import Notification
from django.http import JsonResponse
from functions.text import process_content


def notifications_view(request):
    if not request.user.is_authenticated:
        return redirect('login_url')

    # Получение непрочитанных и прочитанных уведомлений
    unread_notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    read_notifications = Notification.objects.filter(recipient=request.user, is_read=True).order_by('-created_at')[:20]

    # Объединение списков уведомлений
    all_notifications = list(unread_notifications) + list(read_notifications)

    # Обработка уведомлений с помощью process_content
    processed_messages = {notif: process_content(notif.message) for notif in all_notifications}

    # Передаем уведомления в шаблон
    context = {
        'unread_notifications': unread_notifications,
        'read_notifications': read_notifications,
        'processed_messages': processed_messages
    }

    # Обновляем статус уведомлений на "прочитанные" после того, как они были получены
    # unread_notifications.update(is_read=True)

    return render(request, 'notifications/notifications.html', context)



def mark_notifications_as_read(request):
    if request.user.is_authenticated and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False}, status=403)