"""Здесь будем тестировать маршруты."""
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note
from .utils import BaseTestCase

User = get_user_model()


class TestRoutes(BaseTestCase):
    """класс для тестов маршрутов."""

    @classmethod
    def setUpTestData(cls):
        """Дополнительные фикстуры, специфичные для тестов редактирования."""
        super().setUpTestData()

        cls.author_client = cls.client_class()
        cls.author_client.force_login(cls.author)

        cls.reader_client = cls.client_class()
        cls.reader_client.force_login(cls.reader)

        cls.note = Note.objects.create(
            text=cls.NOTE_TEXT,
            title='Заголовок заметки',
            slug='note-slug',
            author=cls.author,
        )

        cls.NOTES_EDIT_URL = reverse('notes:edit', args=(cls.note.slug,))
        cls.NOTES_DETAIL_URL = reverse('notes:detail', args=(cls.note.slug,))
        cls.NOTES_DELETE_URL = reverse('notes:delete', args=(cls.note.slug,))

    def test_pages_availability(self):
        """универсальный тест доступности страницы."""
        clients = [
            (self.client, (self.NOTES_HOME_URL, self.LOGIN_URL,
                           self.LOGOUT_URL, self.SIGNUP_URL)),
            (self.reader_client, (self.NOTES_LIST_URL, self.NOTES_ADD_URL,
                                  self.NOTES_SUCCESS_URL)),
            (self.author_client, (self.NOTES_DETAIL_URL, self.NOTES_EDIT_URL,
                                  self.NOTES_DELETE_URL)),
        ]
        for client, urls in clients:
            for url in urls:
                with self.subTest(url=url):
                    response = client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_unavailability(self):
        """универсальный тест недоступности страницы."""
        clients = [
            (self.reader_client, (self.NOTES_DETAIL_URL, self.NOTES_EDIT_URL,
                                  self.NOTES_DELETE_URL)),
        ]
        for client, urls in clients:
            for url in urls:
                with self.subTest(url=url):
                    response = client.get(url)
                    self.assertEqual(response.status_code,
                                     HTTPStatus.NOT_FOUND)

    def test_redirect_for_anonymous_client(self):
        """Проверка, что анонима отправят регистрироваться."""
        urls = (self.NOTES_ADD_URL, self.NOTES_EDIT_URL, self.NOTES_DETAIL_URL,
                self.NOTES_DELETE_URL, self.NOTES_LIST_URL,
                self.NOTES_SUCCESS_URL)
        for name in urls:
            with self.subTest(name=name):
                redirect_url = f'{self.LOGIN_URL}?next={name}'
                response = self.client.get(name)
                self.assertRedirects(response, redirect_url)
