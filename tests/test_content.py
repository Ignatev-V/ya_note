"""тестирование контента."""
from notes.forms import NoteForm
from .utils import BaseTestCase


class TestContent(BaseTestCase):
    """Класс под тесты контента."""

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
