"""тестирование контента."""
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import NoteForm
from .utils import BaseTestCase


User = get_user_model()


class TestContent(BaseTestCase):
    """Класс под тесты контента."""

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

    def test_note_in_list_for_author(self):
        """Проверка, что заметка попадает в список автора."""
        response = self.author_client.get(self.NOTES_LIST_URL)
        self.assertIn(self.note, response.context['object_list'])

    def test_note_not_in_list_for_another_user(self):
        """Заметки нет в чужом списке."""
        response = self.reader_client.get(self.NOTES_LIST_URL)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_note_pages_contain_form(self):
        """Страницы добавление и редактирования содержат формы."""
        urls = (self.NOTES_ADD_URL, self.NOTES_EDIT_URL)
        for name in urls:
            with self.subTest(name=name):
                response = self.author_client.get(name)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
