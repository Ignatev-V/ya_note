"""тестирование логики."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestNotesEdit(TestCase):
    """Класс для тестов логики редактирования заметок."""

    NOTE_TEXT = 'Текст заметки'
    NOTE_EDIT_TEXT = 'Измененный текст комментария'

    @classmethod
    def setUpTestData(cls):
        """Фикстурки для тестирования логики редактирования заметок."""
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(title='Заголовок',
                                       text=cls.NOTE_TEXT,
                                       slug='NightsNotes',
                                       author=cls.author,
                                       )
        cls.url = reverse('notes:edit', args=(cls.note.slug,))
        cls.form_data = {
            'title': cls.note.title,
            'text': cls.NOTE_EDIT_TEXT,
        }

    def test_anonymous_user_cant_edit_note(self):
        """Проверка, что аноним не может редачить заметки."""
        self.client.post(self.url, data=self.form_data)
        note_text = Note.objects.get(slug=self.note.slug).text
        self.assertEqual(note_text, self.NOTE_TEXT)

    def test_user_cant_edit_another_user_note(self):
        """Проверка, что нельзя редачить чужик записи."""
        self.client.force_login(self.reader)
        self.client.post(self.url, data=self.form_data)
        note_text = Note.objects.get(slug=self.note.slug).text
        self.assertEqual(note_text, self.NOTE_TEXT)

    def test_user_can_edit_note(self):
        """Проверка, что автор может редачить заметку."""
        self.client.force_login(self.author)
        self.client.post(self.url, data=self.form_data)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_EDIT_TEXT)
