"""Цей модуль використовується для розміщення представлень додатку "comments"."""

from typing import Any, NoReturn

from django import http
from django.views import generic
from django.contrib import messages

from . import services
from .models import Comment
from .forms import CommentModelForm
from general.views import BaseView


FORM_DATA = {}


class CommentListView(BaseView, generic.ListView):
    """Представлення для відображення всіх коментарів."""

    paginate_by = 25
    queryset = Comment.objects.all().filter(parent_id__isnull=True)

    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse | NoReturn:
        """Цей метод перевіряє порядок сортування та викликає метод get батьківського класу.

        Raises:
            404: Якщо порядок сортування неправильний.

        Returns:
            get: Відповідь на HTTP-запит.
        """
        if self.get_ordering() is None:
            raise http.Http404
        return super().get(request, *args, **kwargs)

    def get_ordering(self) -> str | None:
        """Цей метод повертає рядок сортування або None за GET-параметрами.

        Returns:
            get_ordering_string: Рядок сортування або None.
        """
        return services.get_ordering_string(
            self.request.GET.get("orderby") or "c",
            self.request.GET.get("orderdir") or "desc",
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Цей метод додає форму до контексту та повертає його.

        Returns:
            context: Контекст представлення.
        """
        global FORM_DATA
        context = super().get_context_data(**kwargs)
        context["form"] = CommentModelForm(FORM_DATA or None)
        FORM_DATA = {}
        return context


class CommentCreateView(BaseView, generic.CreateView):
    """Представлення для обробки тільки запиту POST та створення коментаря."""

    model = Comment
    success_url = "/"
    http_method_names = ["post"]
    form_class = CommentModelForm

    def form_valid(self, form: CommentModelForm) -> http.HttpResponseRedirect:
        """Цей метод зберігає форму, додає повідомлення про успіх та повертає перенаправлення на success_url.

        Args:
            form (CommentModelForm): Валідна форма.

        Returns:
            success_url: Перенаправлення на success_url.
        """
        comment_parent_id = self.request.POST.get("comment_parent_id", None)
        canvas_url = self.request.POST.get("resized_image", None)
        form.save(comment_parent_id, canvas_url)

        s = "comment" if not comment_parent_id else "answer"
        messages.success(self.request, f"Your {s} has successfully added.")
        return http.HttpResponseRedirect(self.success_url)

    def form_invalid(
        self, form: CommentModelForm
    ) -> http.HttpResponseRedirect:
        """Цей метод додає повідомлення про помилку та повертає перенаправлення на success_url.

        Args:
            form (CommentModelForm): Невалідна форма.

        Returns:
            success_url: Перенаправлення на success_url.
        """
        global FORM_DATA
        FORM_DATA = self.request.POST

        messages.error(self.request, "Invalid form data.")
        return http.HttpResponseRedirect(self.success_url)
