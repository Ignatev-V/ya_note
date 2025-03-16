"""Вынесенные константы для тестов."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class BaseTestCase(TestCase):
    """Базовый класс с фикстурами для тестов заметок."""

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
        }

        cls.author_client = cls.client_class()
        cls.author_client.force_login(cls.author)

        cls.reader_client = cls.client_class()
        cls.reader_client.force_login(cls.reader)

        cls.note = Note.objects.create(
            text='Текст заметки',
            title='Заголовок заметки',
            slug='note-slug',
            author=cls.author,
        )

        cls.LOGIN_URL = reverse('users:login')
        cls.LOGOUT_URL = reverse('users:logout')
        cls.NOTES_ADD_URL = reverse('notes:add')
        cls.NOTES_HOME_URL = reverse('notes:home')
        cls.NOTES_LIST_URL = reverse('notes:list')
        cls.NOTES_SUCCESS_URL = reverse('notes:success')
        cls.SIGNUP_URL = reverse('users:signup')
        cls.NOTES_EDIT_URL = reverse('notes:edit', args=(cls.note.slug,))
        cls.NOTES_DETAIL_URL = reverse('notes:detail', args=(cls.note.slug,))
        cls.NOTES_DELETE_URL = reverse('notes:delete', args=(cls.note.slug,))
