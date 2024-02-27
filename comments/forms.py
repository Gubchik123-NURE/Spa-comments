"""Цей модуль використовується для розміщення класів форм додатку 'comments'."""

import base64

from django import forms
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from captcha.fields import CaptchaField, CaptchaTextInput
from django.contrib.auth.validators import UnicodeUsernameValidator

from .models import Author, Comment


FIELD_WIDGET_ATTRS = {"class": "form-control mb-1"}


class CommentModelForm(forms.ModelForm):
    """Форма моделі для моделі коментарів для створення коментаря."""

    username = forms.CharField(
        max_length=100,
        min_length=2,
        required=True,
        validators=[UnicodeUsernameValidator()],
        widget=forms.TextInput(attrs=FIELD_WIDGET_ATTRS),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs=FIELD_WIDGET_ATTRS),
    )
    captcha = CaptchaField(widget=CaptchaTextInput(attrs=FIELD_WIDGET_ATTRS))

    def save(
        self,
        comment_parent_id: str | None,
        canvas_url: str | None,
        commit=False,
    ) -> None:
        """Цей метод створює коментар для нового або існуючого автора.

        Args:
            comment_parent_id (str): Ідентифікатор батьківського коментаря.
            canvas_url (str): URL-адреса зображення в форматі base64.
            commit (bool): Зберегти коментар у базі даних.
        """
        comment: Comment = super().save(commit)

        if comment_parent_id and comment_parent_id.isdigit():
            comment.parent = get_object_or_404(
                Comment, id=int(comment_parent_id)
            )
        comment.author = self.get_author()

        if canvas_url:
            comment.file.save(
                comment.file.name,
                self.get_image_file_from_(canvas_url, comment.file.name),
            )
        comment.save()

    def get_author(self) -> Author:
        """Цей метод повертає нового або існуючого автора.

        Returns:
            Автор: Новий або існуючий автор.
        """
        author, _ = Author.objects.get_or_create(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
        )
        return author

    def get_image_file_from_(
        self, canvas_url: str, filename: str
    ) -> ContentFile:
        """Returns content file from decoded canvas_url."""
        """Цей метод повертає файл зображення з декодованої URL-адреси canvas_url.

        Returns:
            Файл: зображення.
        """
        image_data = canvas_url.split(",")[1]
        return ContentFile(base64.b64decode(image_data), name=filename)

    class Meta:
        """Мета-опції для CommentModelForm."""

        model = Comment
        fields = ("username", "email", "home_page", "captcha", "text", "file")
        labels = {
            "home_page": "Home page (optional)",
            "file": "Attached comment file (optional)",
        }
        widgets = {
            "home_page": forms.URLInput(attrs=FIELD_WIDGET_ATTRS),
            "text": forms.Textarea(attrs=FIELD_WIDGET_ATTRS),
            "file": forms.FileInput(
                attrs={
                    "class": "form-control mb-1",
                    "accept": ".jpg, .jpeg, .gif, .png, .txt",
                }
            ),
        }
