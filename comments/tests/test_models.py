"""Цей модуль містить тести для моделей додатку 'comments'."""

from django.test import TestCase
from django.db.models import Model

from comments.models import Author, Comment


class _ModelMetaOptionsTestMixin:
    """Mixin для тестування базових мета-опцій моделей."""

    model: Model
    verbose_name: str
    verbose_name_plural: str
    ordering: list[str]

    def test_model_verbose_name(self):
        """Цей метод тестує, що назва багатослівної моделі дорівнює атрибуту verbose_name."""
        self.assertEqual(self.model._meta.verbose_name, self.verbose_name)

    def test_model_verbose_name_plural(self):
        """Цей метод тестує, що назва багатослівної моделі (множина) дорівнює атрибуту verbose_name_plual."""
        self.assertEqual(
            self.model._meta.verbose_name_plural, self.verbose_name_plural
        )

    def test_model_fields_ordering(self):
        """Цей метод тестує, що впорядкування моделі дорівнює атрибуту впорядкування."""
        self.assertEqual(self.model._meta.ordering, self.ordering)


class AuthorModelTestCase(_ModelMetaOptionsTestMixin, TestCase):
    """Тести для моделі автора."""

    model = Author
    ordering = ["username"]
    verbose_name = "Comment author"
    verbose_name_plural = "Comment authors"

    @classmethod
    def setUpTestData(cls) -> None:
        """Цей метод створює першого автора для тестування."""
        Author.objects.create(username="test_user", email="test@gmail.com")

    def test_model_string_representation(self):
        """Цей метод тестує рядкове представлення моделі за допомогою __str__."""
        obj = self.model.objects.first()
        self.assertEqual(str(obj), obj.username)

    # * ---------------- Test the 'username' field parameters -----------------

    def test_username_max_length(self):
        """Цей метод тестує, що поле імені користувача має max_length = 100."""
        self.assertEqual(
            self.model._meta.get_field("username").max_length, 100
        )

    def test_username_unique(self):
        """Цей метод тестує, що поле імені користувача є унікальним = помилково."""
        self.assertFalse(self.model._meta.get_field("username").unique)

    def test_username_blank(self):
        """Цей метод тестує, що поле імені користувача порожнє = помилково."""
        self.assertFalse(self.model._meta.get_field("username").blank)

    def test_username_null(self):
        """Цей метод тестує, що поле імені користувача є null = false."""
        self.assertFalse(self.model._meta.get_field("username").null)

    def test_username_verbose_name(self):
        """Цей метод тестує, що поле імені користувача має verbose_name = 'ім'я користувача'."""
        self.assertEqual(
            self.model._meta.get_field("username").verbose_name, "Username"
        )

    # * ----------------- Test the 'email' field parameters -------------------

    def test_email_unique(self):
        """Цей метод тестує, що поле електронної пошти є унікальним = помилково."""
        self.assertFalse(self.model._meta.get_field("email").unique)

    def test_email_blank(self):
        """Цей метод тестує, що поле електронної пошти порожнє = помилково."""
        self.assertFalse(self.model._meta.get_field("email").blank)

    def test_email_null(self):
        """Цей метод тестує, що поле електронної пошти null = false."""
        self.assertFalse(self.model._meta.get_field("email").null)

    def test_email_verbose_name(self):
        """Цей метод тестує, що поле електронної пошти має verbose_name = 'адреса електронної пошти'."""
        self.assertEqual(
            self.model._meta.get_field("email").verbose_name, "Email address"
        )


class CommentModelTestCase(_ModelMetaOptionsTestMixin, TestCase):
    """Тести для моделі коментарів."""

    model = Comment
    ordering = ["-created"]
    verbose_name = "Comment"
    verbose_name_plural = "Comments"

    @classmethod
    def setUpTestData(cls) -> None:
        """Цей метод створює перший коментар для тестування."""
        cls.author = Author.objects.create(
            username="test_user", email="test@gmail.com"
        )
        Comment.objects.create(
            text="test comment", author=cls.author, parent=None
        )

    def test_model_string_representation(self):
        """Цей метод тестує рядкове представлення моделі за допомогою __str__."""
        obj = self.model.objects.first()
        self.assertEqual(str(obj), f"{obj.pk} from {obj.author}")

    # * ---------------- Test the 'home_page' field parameters ----------------

    def test_home_page_blank(self):
        """Цей метод тестує, що поле Home_Page порожнє = правда."""
        self.assertTrue(self.model._meta.get_field("home_page").blank)

    def test_home_page_null(self):
        """Цей метод тестує, що поле Home_Page є null = true."""
        self.assertTrue(self.model._meta.get_field("home_page").null)

    def test_home_page_verbose_name(self):
        """Цей метод тестує, що поле Home_Page має verbose_name = 'домашня сторінка'."""
        self.assertEqual(
            self.model._meta.get_field("home_page").verbose_name, "Home page"
        )

    # * ---------------- Test the 'text' field parameters ---------------------

    def test_text_blank(self):
        """Цей метод тестує, що текстове поле порожнє = помилково."""
        self.assertFalse(self.model._meta.get_field("text").blank)

    def test_text_null(self):
        """Цей метод тестує, що текстове поле є null = false."""
        self.assertFalse(self.model._meta.get_field("text").null)

    def test_text_verbose_name(self):
        """Цей метод тестує, що текстове поле має verbose_name = 'body comment'."""
        self.assertEqual(
            self.model._meta.get_field("text").verbose_name, "Comment body"
        )

    # * ----------------- Test the 'file' field parameters --------------------

    def test_file_upload_to(self):
        """Цей метод тестує, що поле файлу має upload_to = 'comment_files/'."""
        self.assertEqual(
            self.model._meta.get_field("file").upload_to, "comment_files/"
        )

    def test_file_blank(self):
        """Цей метод тестує, що поле файлу порожнє = правда."""
        self.assertTrue(self.model._meta.get_field("file").blank)

    def test_file_null(self):
        """Цей метод тестує, що поле файлу є null = true."""
        self.assertTrue(self.model._meta.get_field("file").null)

    def test_file_verbose_name(self):
        """Цей метод тестує, що поле файлу має verbose_name = 'доданий файл коментарів'."""
        self.assertEqual(
            self.model._meta.get_field("file").verbose_name,
            "Attached comment file",
        )

    # * ---------------- Test the 'created' field parameters ------------------

    def test_created_auto_now_add(self):
        """Цей метод тестує, що створене поле має auto_now_add = true."""
        self.assertTrue(self.model._meta.get_field("created").auto_now_add)

    def test_created_verbose_name(self):
        """Цей метод тестує, що створене поле має verbose_name = 'створений dateTime'."""
        self.assertEqual(
            self.model._meta.get_field("created").verbose_name,
            "Created datetime",
        )

    # * ---------------- Test the 'parent' field parameters -------------------

    def test_parent_null(self):
        """Цей метод тестує, що батьківське поле є null = true."""
        self.assertTrue(self.model._meta.get_field("parent").null)

    def test_parent_blank(self):
        """Цей метод тестує, що батьківське поле порожнє = правда."""
        self.assertTrue(self.model._meta.get_field("parent").blank)

    def test_parent_default(self):
        """Тести, які батьківське поле має за замовчуванням = немає."""
        self.assertIsNone(self.model._meta.get_field("parent").default)

    def test_parent_verbose_name(self):
        """Цей метод тестує, що батьківське поле має verbose_name = 'батьківський коментар'."""
        self.assertEqual(
            self.model._meta.get_field("parent").verbose_name, "Parent comment"
        )

    def test_parent_on_delete(self):
        """Цей метод тестує, що батьківське поле on_delete є каскадом."""
        Comment.objects.get(id=1).delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=1)

    # * ---------------- Test the 'author' field parameters -------------------

    def test_author_verbose_name(self):
        """Цей метод тестує, що поле автора має verbose_name = 'автор коментарів'."""
        self.assertEqual(
            self.model._meta.get_field("author").verbose_name, "Comment author"
        )

    def test_author_on_delete(self):
        """Цей метод тестує, що авторське поле on_delete є каскадом."""
        Comment.objects.get(id=1).delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=1)
