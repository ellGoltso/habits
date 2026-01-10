from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Кастомная модель пользователя.
    """
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': "Пользователь с таким email уже существует.",
        },
    )
    bio = models.TextField('О себе', max_length=500, blank=True, null=True)
    avatar = models.ImageField('Аватар', upload_to='users/avatars/', blank=True, null=True)
    phone = models.CharField('Номер телефона', max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
