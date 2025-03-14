"""Создание пользователей и клиентов."""
from django.test import Client
from django.contrib.auth.models import User


def create_users(func):
    """Создаем пользователей."""
    def wrapper(cls):
        author = User.objects.create(username='Лев Толстой')
        author_client = Client()
        author_client.force_login(author)
        user = User.objects.create(username='Читатель')
        user_client = Client()
        user_client.force_login(user)
        func(cls, author, author_client, user, user_client)
    return wrapper
