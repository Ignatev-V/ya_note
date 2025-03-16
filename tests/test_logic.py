"""тестирование логики."""
from http import HTTPStatus

from django.contrib.auth import get_user
from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING
from .utils import BaseTestCase


class TestNotesEdit(BaseTestCase):
    """Класс для тестов логики редактирования заметок."""

    def test_authenticated_user_can_create_note(self):
        """Неаноним может писать заметки."""
        Note.objects.all().delete()
        response = self.author_client.post(self.NOTES_ADD_URL,
                                           data=self.form_data)
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, get_user(self.author_client))

    def test_anonymous_user_cannot_create_note(self):
        """Аноним не может писать заметки."""
        notes_count_before = Note.objects.count()
        response = self.client.post(self.NOTES_ADD_URL, self.form_data)
        expected_url = f'{self.LOGIN_URL}?next={self.NOTES_ADD_URL}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), notes_count_before)

    def test_not_unique_slug(self):
        """Проверка уникальности SLUG."""
        notes_count_before = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(
            self.NOTES_ADD_URL,
            data=self.form_data)
        self.assertEqual(Note.objects.count(), notes_count_before)
        self.assertFormError(
            response, "form", "slug", errors=(self.note.slug + WARNING)
        )

    def test_empty_slug(self):
        """Пустой слуг недопустим и формируется."""
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.author_client.post(self.NOTES_ADD_URL,
                                           data=self.form_data)
        self.assertEqual(Note.objects.count(), 1)
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        """Создатель может редачить заметку."""
        response = self.author_client.post(self.NOTES_EDIT_URL,
                                           data=self.form_data)
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        new_note = Note.objects.get(id=self.note.id)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.note.author)

    def test_author_can_delete_note(self):
        """Создатель может удалить заметку."""
        notes_count_before = Note.objects.count()
        response = self.author_client.post(self.NOTES_DELETE_URL)
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), notes_count_before - 1)

    def test_other_user_cant_edit_note(self):
        """Нельзя редактировать чужую заметку."""
        response = self.reader_client.post(self.NOTES_EDIT_URL, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_other_user_cant_delete_note(self):
        """Чужую заметку удалить нельзя."""
        notes_count_before = Note.objects.count()
        response = self.reader_client.post(self.NOTES_DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), notes_count_before)
