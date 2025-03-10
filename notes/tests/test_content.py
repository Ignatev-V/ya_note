"""тестирование контента."""

import unittest
from datetime import datetime, timedelta

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from notes.models import Note

User = get_user_model()


class TestHomePage(TestCase):
    """Класс под тесты Главной страницы."""

    HOME_URL = reverse('notes:home')

    @classmethod
    def setUpTestData(cls):
        """Фикстура класса."""
        cls.author = User.objects.create(username='А.С.Пушкин')
        all_notes = [
            Note(
                title=f'Новость {index}',
                text='Просто текст.',
                slug=f'NightsBred{index}',
                author=cls.author,
            )
            for index in range(settings.NOTES_COUNT_ON_HOME_PAGE + 1)
        ]
        Note.objects.bulk_create(all_notes)
        cls.list_url = reverse('notes:list')

    @unittest.expectedFailure
    def test_notes_count(self):
        """Проверяем максимальное количество новостей на Главной."""
        self.client.force_login(self.author)
        response = self.client.get(self.list_url)
        object_list = response.context['object_list']
        notes_count = object_list.count()
        self.assertEqual(notes_count, settings.NOTES_COUNT_ON_HOME_PAGE)

    def test_news_order(self):
        """Проверяем что список заметок отсортирован по дате.
        
        Ориентируем на ID заметки"""
        self.client.force_login(self.author)
        response = self.client.get(self.list_url)
        object_list = response.context['object_list']
        all_ids = [note.id for note in object_list]
        sorted_dates = sorted(all_ids)
        self.assertEqual(all_ids, sorted_dates)
