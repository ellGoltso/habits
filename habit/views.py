from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Habit
from .paginators import HabitPaginator
from .serializers import HabitSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список личных привычек",
        description="Возвращает только те привычки, которые создал текущий пользователь.",
    ),
    create=extend_schema(
        summary="Создание привычки",
        description="Валидация: время < 120 сек, периодичность <= 7 дней.",
    ),
)
class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с личными привычками.
    Доступ: только авторизованный владелец.
    """

    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [permissions.IsAuthenticated]
    queryset = Habit.objects.all()

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        summary="Список публичных привычек",
        description="Доступно всем авторизованным пользователям.",
    ),
)
class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра публичных привычек.
    Доступ: чтение доступно авторизованным, редактирование запрещено.
    """

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
