from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from habit.models import Habit
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com", username="testuser")
        self.user.set_password('testpassword')
        self.user.save()

        self.client.force_authenticate(user=self.user)

        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="10:00:00",
            action="Съесть яблоко",
            is_pleasant=True,
            duration=timedelta(seconds=60)
        )

    def test_create_habit(self):
        """Тест успешного создания привычки"""
        data = {
            "place": "Зал",
            "time": "12:00:00",
            "action": "Бег",
            "duration": "00:02:00",
            "reward": "Отдых",
            "periodicity": 1
        }
        response = self.client.post(reverse('habit:my_habits-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.filter(action="Бег").count(), 1)

    def test_validation_duration(self):
        """Тест: время выполнения не более 120 секунд"""
        data = {
            "place": "Зал",
            "time": "12:00:00",
            "action": "Бег",
            "duration": "00:03:00", # 180 секунд (ошибка)
        }
        response = self.client.post(reverse('habit:my_habits-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Время выполнения не должно превышать 120 секунд", str(response.data))

    def test_validation_reward_and_related(self):
        """Тест: нельзя одновременно reward и related_habit"""
        data = {
            "place": "Зал",
            "time": "12:00:00",
            "action": "Бег",
            "duration": "00:01:00",
            "reward": "Шоколад",
            "related_habit": self.pleasant_habit.id
        }
        response = self.client.post(reverse('habit:my_habits-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_habits(self):
        """Тест: пользователь видит только свои привычки"""
        response = self.client.get(reverse('habit:my_habits-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_public_habits(self):
        """Тест: просмотр публичных привычек доступен всем"""
        self.pleasant_habit.is_public = True
        self.pleasant_habit.save()

        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('habit:public_habits-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
