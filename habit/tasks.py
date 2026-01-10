from celery import shared_task
from django.utils import timezone
from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminders():
    now = timezone.localtime().time()
    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)

    for habit in habits:
        if habit.user.telegram_id:
            message = f"Напоминание: {habit.action} в {habit.place}!"
            send_telegram_message(habit.user.telegram_id, message)
