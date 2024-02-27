"""Цей модуль містить тести для форм додатку 'comments'."""

from django import forms
from django.test import SimpleTestCase
from captcha.fields import CaptchaTextInput
from django.contrib.auth.validators import UnicodeUsernameValidator

from comments.models import Comment
from comments.forms import CommentModelForm, FIELD_WIDGET_ATTRS


FIELD_WIDGET_CLASS = FIELD_WIDGET_ATTRS["class"]


class CommentModelFormSimpleTestCase(SimpleTestCase):
    """Тести для CommentModelForm."""

    @classmethod
    def setUpClass(cls) -> None:
        """Налаштуйте CommentModelform для тестування."""
        super().setUpClass()
        cls.form = CommentModelForm()

    # * ---------- Testing the meta options of the CommentModelForm -----------

    def test_form_model(self):
        """Цей метод тестує модель форми."""
        self.assertEqual(self.form._meta.model, Comment)

    def test_form_fields(self):
        """Цей метод тестує поля форми."""
        self.assertEqual(
            tuple(self.form._meta.fields),
            ("username", "email", "home_page", "captcha", "text", "file"),
        )

    def test_home_page_label(self):
        """Цей метод тестує етикетку домашньої сторінки."""
        self.assertEqual(
            self.form.fields["home_page"].label, "Home page (optional)"
        )

    def test_file_label(self):
        """Цей метод тестує мітку файлу."""
        self.assertEqual(
            self.form.fields["file"].label, "Attached comment file (optional)"
        )

    def test_home_page_widget(self):
        """Цей метод тестує віджет домашньої сторінки."""
        self.assertIsInstance(
            self.form.fields["home_page"].widget, forms.URLInput
        )

    def test_home_page_widget_attrs_class(self):
        """Цей метод виконує тестування класу атринтів віджетів домашньої сторінки."""
        self.assertEqual(
            self.form.fields["home_page"].widget.attrs["class"],
            FIELD_WIDGET_CLASS,
        )

    def test_text_widget(self):
        """Цей метод тестує текстовий віджет."""
        self.assertIsInstance(self.form.fields["text"].widget, forms.Textarea)

    def test_text_widget_attrs_class(self):
        """Цей метод виконує тестування класу атринтів віджетів домашньої сторінки."""
        self.assertEqual(
            self.form.fields["home_page"].widget.attrs["class"],
            FIELD_WIDGET_CLASS,
        )

    def test_file_widget(self):
        """Цей метод тестує віджет файлу."""
        self.assertIsInstance(self.form.fields["file"].widget, forms.FileInput)

    def test_file_widget_attrs_class(self):
        """Цей метод виконує тестування класу віджетів файлів."""
        self.assertEqual(
            self.form.fields["file"].widget.attrs["class"],
            FIELD_WIDGET_CLASS,
        )

    def test_file_widget_attrs_accept(self):
        """Цей метод виконує тестування атрибутів віджетів Файл приймають."""
        self.assertEqual(
            self.form.fields["file"].widget.attrs["accept"],
            ".jpg, .jpeg, .gif, .png, .txt",
        )

    # * ---------------- Test the 'username' field parameters -----------------

    def test_username_max_length(self):
        """Цей метод тестує максимальну довжину імені користувача."""
        self.assertEqual(self.form.fields["username"].max_length, 100)

    def test_username_min_length(self):
        """Цей метод тестує довжину мінімального імені користувача."""
        self.assertEqual(self.form.fields["username"].min_length, 2)

    def test_username_required(self):
        """Цей метод тестує необхідне ім'я користувача."""
        self.assertTrue(self.form.fields["username"].required)

    def test_username_validator(self):
        """Цей метод тестує валідатор користувача."""
        self.assertIsInstance(
            self.form.fields["username"].validators[0],
            UnicodeUsernameValidator,
        )

    def test_username_widget(self):
        """Цей метод тестує віджет користувача."""
        self.assertIsInstance(
            self.form.fields["username"].widget, forms.TextInput
        )

    def test_username_widget_attrs_class(self):
        """Цей метод виконує тестування класу атринтів віджетів користувача."""
        self.assertEqual(
            self.form.fields["username"].widget.attrs["class"],
            FIELD_WIDGET_CLASS,
        )

    # * ---------------- Test the 'email' field parameters --------------------

    def test_email_required(self):
        """Цей метод тестує необхідний електронний лист."""
        self.assertTrue(self.form.fields["email"].required)

    def test_email_widget(self):
        """Цей метод тестує віджет електронної пошти."""
        self.assertIsInstance(
            self.form.fields["email"].widget,
            forms.EmailInput,
        )

    def test_email_widget_attrs_class(self):
        """Цей метод виконує тестування класу атринтів віджетів електронної пошти."""
        self.assertEqual(
            self.form.fields["email"].widget.attrs["class"],
            FIELD_WIDGET_CLASS,
        )

    # * ---------------- Test the 'captcha' field parameters ------------------

    def test_captcha_widget(self):
        """Випробує віджет Captcha."""
        self.assertIsInstance(
            self.form.fields["captcha"].widget, CaptchaTextInput
        )
