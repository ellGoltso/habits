from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель",
        related_name="habits",
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")

    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Используется только для полезных привычек",
    )

    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Периодичность (в днях)",
        help_text="Как часто выполнять (1 — ежедневно, максимум 7)",
    )

    reward = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Вознаграждение"
    )

    duration = models.DurationField(
        verbose_name="Время на выполнение", help_text="Не более 120 секунд (0:02:00)"
    )

    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["id"]

    def __str__(self):
        return f"{self.user} будет {self.action} в {self.time} в {self.place}"

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя одновременно выбрать вознаграждение и связанную привычку."
            )

        if self.duration and self.duration > timedelta(seconds=120):
            raise ValidationError(
                "Время выполнения не должно превышать 120 секунд (2 минуты)."
            )

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError(
                "Связанная привычка должна иметь признак приятной привычки."
            )

        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        if self.periodicity > 7:
            raise ValidationError("Периодичность не должна превышать 7 дней.")

        super().clean()
