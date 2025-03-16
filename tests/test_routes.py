"""Здесь будем тестировать маршруты."""
from http import HTTPStatus

from .utils import BaseTestCase


class TestRoutes(BaseTestCase):
    """Класс для тестов маршрутов."""

    def test_pages_availability(self):
        """Универсальный тест доступности страницы."""
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
        """Универсальный тест недоступности страницы."""
        urls = (self.NOTES_DETAIL_URL, self.NOTES_EDIT_URL,
                self.NOTES_DELETE_URL)
        for url in urls:
            with self.subTest(url=url):
                response = self.reader_client.get(url)
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
