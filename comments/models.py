"""Цей модуль використовується для розміщення моделей додатку 'comments'."""

from django.db import models


class Author(models.Model):
    """Модель, що представляє автора коментарів."""

    username = models.CharField(
        max_length=100,
        unique=False,
        blank=False,
        null=False,
        verbose_name="Username",
    )
    email = models.EmailField(
        unique=False, blank=False, null=False, verbose_name="Email address"
    )

    def __str__(self) -> str:
        """Цей магічний метод повертає рядкове представлення моделі авторів коментарів.

        Returns:
            рядок: нікнейм автора коментаря.
        """
        return self.username

    class Meta:
        """Мета-опції для моделі авторів коментарів."""

        ordering = ["username"]
        verbose_name = "Comment author"
        verbose_name_plural = "Comment authors"


class _CommentCustomManager(models.Manager):
    """Спеціальний менеджер для моделі коментарів."""

    def all(self):
        """Цей метод повертає всі коментарі, використовуючи select_related для 'parent' та 'author'.

        Returns:
            QuerySet: Всі коментарі з вибраними пов'язаними об'єктами.
        """
        return super().all().select_related("parent", "author")


class Comment(models.Model):
    """Модель, що представляє коментар."""

    home_page = models.URLField(
        blank=True, null=True, verbose_name="Home page"
    )
    text = models.TextField(
        blank=False, null=False, verbose_name="Comment body"
    )
    file = models.FileField(
        upload_to="comment_files/",
        blank=True,
        null=True,
        verbose_name="Attached comment file",
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Created datetime"
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="Parent comment",
    )

    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, verbose_name="Comment author"
    )

    objects = _CommentCustomManager()

    def __str__(self) -> str:
        """Цей магічний метод повертає рядкове представлення моделі коментарів.

        Returns:
            рядок: унікальний ідентифікатор коментаря та автора.
        """
        return f"{self.pk} from {self.author}"

    class Meta:
        """Мета-опції для моделі коментарів."""

        ordering = ["-created"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
