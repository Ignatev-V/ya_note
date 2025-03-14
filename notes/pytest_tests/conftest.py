"""Фикстуры для проекта."""
# conftest.py
import pytest

# Импортируем класс клиента.
from django.test.client import Client

# Импортируем модель заметки, чтобы создать экземпляр.
from notes.models import Note


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):
    """Фикстура создания автора."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    """Фикстура не для автора."""
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    """Вызываем фикстуру автора."""
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def not_author_client(not_author):
    """Фикстура создания клиента НеАвтора."""
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
def note(author):
    """Фикстура создания заметки Автором."""
    note = Note.objects.create(  # Создаём объект заметки.
        title='Заголовок',
        text='Текст заметки',
        slug='note-slug',
        author=author,
    )
    return note


@pytest.fixture
def slug_for_args(note):
    """Фикстура запрашивает другую фикстуру создания заметки."""
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return (note.slug,)


# Добавляем фикстуру form_data
@pytest.fixture
def form_data():
    """Фикстура данных в форме Новости."""
    return {
        'title': 'Новый заголовок',
        'text': 'Новый текст',
        'slug': 'new-slug'
    }
