"""Вынесенные константы для тестов."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class BaseTestCase(TestCase):
    """Базовый класс с фикстурами для тестов заметок."""

    NOTE_TEXT = 'Текст заметки'
    NOTE_EDIT_TEXT = 'Измененный текст заметки'

    @classmethod
    def setUpTestData(cls):
        """Создание пользователей и общих данных для всех тестов."""
        cls.author = User.objects.create_user(username='author',
                                              password='password')
        cls.reader = User.objects.create_user(username='user',
                                              password='password')

        cls.form_data = {
            'text': 'Текст',
            'title': 'Название',
            'slug': 'slug_txt',
            'author': cls.author.pk,
        }

        cls.LOGIN_URL = reverse('users:login')
        cls.LOGOUT_URL = reverse('users:logout')
        cls.NOTES_ADD_URL = reverse('notes:add')
        cls.NOTES_HOME_URL = reverse('notes:home')
        cls.NOTES_LIST_URL = reverse('notes:list')
        cls.NOTES_SUCCESS_URL = reverse('notes:success')
        cls.SIGNUP_URL = reverse('users:signup')
