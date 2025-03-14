"""Здесь будем тестировать маршруты."""
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note
from .utils import (NOTES_HOME_URLS, NOTES_EDIT_URLS, NOTES_ADD_URLS,
                    NOTES_DELETE_URLS, NOTES_DETAIL_URLS, NOTES_LIST_URLS,
                    LOGIN_URL, LOGOUT_URL, SIGNUP_URL,
                    NOTES_SUCCESS_URLS)

User = get_user_model()


class TestRoutes(TestCase):
    """класс для тестов."""

    @classmethod
    def setUpTestData(cls):
        """Фикстура."""
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.notes = Note.objects.create(title='Заголовок',
                                        text='Текст',
                                        slug='NightsNotes',
                                        author=cls.author,
                                        )

    def test_pages_availability(self):
        """универсальный тест доступности страницы."""
        urls = (
            (NOTES_HOME_URLS, None),
            (NOTES_ADD_URLS, None),
            (NOTES_EDIT_URLS, (self.notes.slug,)),
            (NOTES_DETAIL_URLS, (self.notes.slug,)),
            (NOTES_DELETE_URLS, (self.notes.slug,)),
            (NOTES_LIST_URLS, None),
            (NOTES_SUCCESS_URLS, None),
            (LOGIN_URL, None),
            (LOGOUT_URL, None),
            (SIGNUP_URL, None),

        )
        self.client.force_login(self.author)
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_note_edit_and_delete(self):
        """проверка доступности редактирования и удаления для автора."""
        self.client.force_login(self.author)
        for name in (NOTES_EDIT_URLS, NOTES_DELETE_URLS, NOTES_DETAIL_URLS):
            with self.subTest(user=self.author, name=name):
                url = reverse(name, args=(self.notes.slug,))
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_cant_edit_another_user(self):
        """Проверка, что простой читатель не может редачить чужие заметки."""
        self.client.force_login(self.reader)
        for name in (NOTES_EDIT_URLS, NOTES_DELETE_URLS, NOTES_DETAIL_URLS):
            with self.subTest(user=self.reader, name=name):
                url = reverse(name, args=(self.notes.slug,))
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_redirect_for_anonymous_client(self):
        """Проверка, что анонима отправят регистрироваться."""
        urls = (
            (NOTES_ADD_URLS, None),
            (NOTES_EDIT_URLS, (self.notes.slug,)),
            (NOTES_DETAIL_URLS, (self.notes.slug,)),
            (NOTES_DELETE_URLS, (self.notes.slug,)),
            (NOTES_LIST_URLS, None),
            (NOTES_SUCCESS_URLS, None),
        )
        login_url = reverse(LOGIN_URL)
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
