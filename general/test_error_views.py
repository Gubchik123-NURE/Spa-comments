"""Цей модуль містить тести для власних обробників помилок."""

from typing import NoReturn

from django.urls import path
from django.views import View
from django.test import TestCase
from django.core.exceptions import BadRequest
from django.http import HttpRequest, HttpResponse, Http404

from general.error_views import (
    ErrorView,
    CustomBadRequestView,
    CustomNotFoundView,
    CustomServerErrorView,
)
from general.views import BaseView
from spa.urls import urlpatterns, handler400, handler404


class RaiseExceptionView(View):
    """Представлення, що кидає атрибут винятку."""

    exception: Exception

    def get(self, request: HttpRequest) -> NoReturn:
        """Raises the specified exception."""
        """Цей метод викликає виняток, який вказаний в атрибуті винятку.

        Raises:
            exception: Виняток, який вказаний в атрибуті винятку.
        """
        raise self.exception


class RaiseBadRequestView(RaiseExceptionView):
    """Представлення, що кидає виняток 400 поганого запиту."""

    exception = BadRequest


class RaiseNotFoundView(RaiseExceptionView):
    """Представлення, що кидає 404, не знайдений винятку."""

    exception = Http404


class ServerErrorView(BaseView, View):
    """Представлення, що має помилку."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Цей метод викликає виняток, перед тим як повернути відповідь.

        Args:
            request: Об'єкт запиту.

        Returns:
            HttpResponse: Відповідь на HTTP-запит.
        """
        print(1 / 0)  # ZeroDivisionError
        return HttpResponse("Some content")


# Adding URLs for testing custom error handlers.
# Because the custom error page extends _base.html,
# where there are some links by view names such as "faq" and "about".
urlpatterns += [
    path("400/", RaiseBadRequestView.as_view()),
    path("404/", RaiseNotFoundView.as_view()),
    path("500/", ServerErrorView.as_view()),
]


class CustomErrorHandlerTestMixin:
    """Тестовий міксин для спеціальних обробників помилок."""

    error_handler: ErrorView

    def setUp(self):
        """Цей метод встановлює відповідь з тестовим клієнтом за згенерованим атрибутом url."""
        self.response = self.client.get(f"/{self.error_handler.code}/")

    def test_view_status_code(self):
        """Цей метод перевіряє, чи статус відповіді відповідає атрибуту коду."""
        self.assertEqual(self.response.status_code, self.error_handler.code)

    def test_view_template(self):
        """Цей метод перевіряє, чи шаблон відповіді відповідає атрибуту template_name."""
        self.assertTemplateUsed(self.response, "error.html")

    def test_view_content(self):
        """Цей метод перевіряє, чи відповідь містить інформацію про помилку."""
        self.assertContains(
            self.response,
            self.error_handler.name,
            status_code=self.error_handler.code,
        )
        self.assertContains(
            self.response,
            self.error_handler.description,
            status_code=self.error_handler.code,
        )


class CustomBadRequestViewTest(CustomErrorHandlerTestMixin, TestCase):
    """Тести для CustomBadRequestView."""

    error_handler = CustomBadRequestView


class CustomNotFoundViewTest(CustomErrorHandlerTestMixin, TestCase):
    """Тести для CustomNotFoundView."""

    error_handler = CustomNotFoundView


class CustomServerErrorViewTest(CustomErrorHandlerTestMixin, TestCase):
    """Тести для CustomServerErrorView."""

    error_handler = CustomServerErrorView
