from rest_framework import viewsets, permissions
from .models import Habit
from .paginators import HabitPaginator
from .serializers import HabitSerializer

class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с личными привычками.
    Доступ: только авторизованный владелец.
    """
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра публичных привычек.
    Доступ: чтение доступно авторизованным, редактирование запрещено.
    """
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
