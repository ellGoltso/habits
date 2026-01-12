from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер для пользователя."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        "email address",
        unique=True,
        error_messages={
            "unique": "Пользователь с таким email уже существует.",
        },
    )

    bio = models.TextField("О себе", max_length=500, blank=True, null=True)
    avatar = models.ImageField("Аватар", upload_to="users/avatars/", blank=True, null=True)
    phone = models.CharField("Номер телефона", max_length=15, blank=True, null=True)
    telegram_id = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="ID чата в Telegram", db_index=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email