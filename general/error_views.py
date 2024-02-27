"""Цей модуль містить класи та функції для візуалізації сторінок помилок."""

from typing import NamedTuple

from django.views import View
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template.exceptions import TemplateDoesNotExist


class Error(NamedTuple):
    """Названий Tuple, який містить інформацію про помилку."""

    code: int
    name: str
    description: str


def render_error_page(request: HttpRequest, error: Error) -> HttpResponse:
    """Ця функція візуалізує сторінку помилки (якщо шаблон існує) за вказаною помилкою.

    Args:
        request: Об'єкт запиту.
        error: Об'єкт помилки.

    Returns:
        render: Сторінка помилки з вказаною інформацією про помилку.
    """
    try:
        return render(
            request, "error.html", {"error": error}, status=error.code
        )
    except TemplateDoesNotExist:
        return HttpResponse(
            f"""
            <title>{error.code} | LapZone</title>
            <h1>{error.name}</h1>
            <h4>{error.description}</h4>
            """,
            status=error.code,
        )


class ErrorView(View):
    """Представлення базової помилки для візуалізації спеціальної сторінки помилок."""

    code: int
    name: str
    description: str

    def get(self, request: HttpRequest, exception=None) -> HttpResponse:
        """Цей метод повертає сторінку помилки з вказаною інформацією про помилку.

        Args:
            request: Об'єкт запиту.
            exception (Exception): Об'єкт винятку.

        Returns:
            HttpResponse: Сторінка помилки з вказаною інформацією про помилку.
        """
        return render_error_page(
            request, Error(self.code, self.name, self.description)
        )


class CustomBadRequestView(ErrorView):
    """Спеціальне представлення для обробки 400 коду статусу HTTP."""

    code = 400
    name = "Bad Request"
    description = "The server cannot or will not process the request."


class CustomNotFoundView(ErrorView):
    """Спеціальне представлення для обробки 404 коду статусу HTTP."""

    code = 404
    name = "Not Found"
    description = (
        "The server cannot find the requested resource. URL is not recognized."
    )


class CustomServerErrorView(ErrorView):
    """Спеціальне представлення для обробки 500 коду статусу HTTP."""

    code = 500
    name = "Internal Server Error"
    description = "Sorry, an error occurred in the server. Try again."
