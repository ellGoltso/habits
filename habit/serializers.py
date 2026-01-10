from rest_framework import serializers
from .models import Habit
from datetime import timedelta


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, data):
        """
        Валидация всех полей (аналог метода clean в модели).
        """
        reward = data.get("reward")
        related_habit = data.get("related_habit")
        is_pleasant = data.get("is_pleasant")
        duration = data.get("duration")
        periodicity = data.get("periodicity")

        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно выбрать вознаграждение и связанную привычку."
            )

        if duration and duration > timedelta(seconds=120):
            raise serializers.ValidationError(
                "Время выполнения не должно превышать 120 секунд."
            )

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной (is_pleasant=True)."
            )

        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        if periodicity and periodicity > 7:
            raise serializers.ValidationError(
                "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
            )

        return data
