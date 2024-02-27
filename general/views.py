"""Цей модуль містить базовий клас для всіх поглядів."""

import logging

from django import http
from django.core.exceptions import BadRequest

from .error_views import Error, CustomServerErrorView, render_error_page

logger = logging.getLogger(__name__)


class BaseView:
    """Базовий вигляд для всіх інших поглядів із обробкою винятків."""

    def dispatch(
        self, request: http.HttpRequest, *args, **kwargs
    ) -> http.HttpResponse:
        """Цей метод викликається при кожному HTTP-запиті до погляду.

        Args:
            request (http.HttpRequest): Об'єкт запиту.

        Raises:
            e: Виняток, який виник під час обробки запиту.

        Returns:
            render_error_page: Відповідь на HTTP-запит.
        """
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            exception_type = type(e)

            # Check if it's an exception for which there is an error handler.
            if exception_type in (http.Http404, BadRequest):
                raise e

            logger.error(
                f"{exception_type}('{str(e)}') during working with {request.path} URL"
            )

            error_view = CustomServerErrorView
            return render_error_page(
                request,
                Error(
                    error_view.code, error_view.name, error_view.description
                ),
            )
