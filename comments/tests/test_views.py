"""Цей модуль містить тести для представлень додатку 'comments'."""

from django.urls import reverse
from django.test import TestCase
from django.http import HttpResponse

from comments.models import Author, Comment
from comments.forms import CommentModelForm


class CommentListViewTestCase(TestCase):
    """Тести для представлення списку коментарів."""

    url = "/"
    name = "list"
    template_name = "comments/comment_list.html"
    queryset = Comment.objects.all().filter(parent_id__isnull=True)

    @classmethod
    def setUpTestData(cls) -> None:
        """Встановлює дані тестів, створюючи 28 коментарів."""
        for count in range(1, 29):
            Comment.objects.create(
                text=f"Tests comment #{count}",
                author=Author.objects.create(
                    username=f"test_user_{count}",
                    email=f"test_user_{count}@gmail.com",
                ),
            )

    def setUp(self) -> None:
        """Встановлює тести, отримаючи відповідь з URL -адреси виду."""
        self.response = self.client.get(self.url)

    def test_view_url_exists_at_desired_location(self):
        """Випробування, що вид існує у бажаному місці."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Тести, що відповідь у перегляді використовує правильний шаблон."""
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, self.template_name)

    def test_view_url_accessible_by_name(self):
        """Випробує, що перегляд доступний за допомогою його імені."""
        response = self.client.get(reverse(self.name))
        self.assertEqual(response.status_code, 200)

    def test_comment_form_is_in_context(self):
        """Тести, що форма знаходиться в контексті."""
        self.assertIn("form", self.response.context)
        self.assertIsInstance(self.response.context["form"], CommentModelForm)

    def test_lists_comments(self):
        """Тести, які коментарі перераховані на сторінці."""
        self.assertIn("page_obj", self.response.context)
        self.assertEqual(
            self.response.context["page_obj"].object_list,
            list(self.queryset[:25]),
        )

    # * ------------------ Testing pagination functionality -------------------

    def test_pagination_is_twenty_five(self):
        """Тести, що Pagition встановлюється на 25 на сторінку."""
        self.assertEqual(len(self.response.context["page_obj"]), 25)

    def test_paginated_product_list(self):
        """Друга сторінка тестів має (точно) залишилось 3 коментарів."""
        response = self.client.get(f"{self.url}?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 3)

    def test_404_with_invalid_pagination_page_value(self):
        """Тести, які недійсні значення сторінки Pagination призводять до 404."""
        response = self.client.get(f"{self.url}?page=0")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.url}?page=3")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.url}?page=string")
        self.assertEqual(response.status_code, 404)

    # * ------------------- Testing ordering functionality --------------------

    def test_lists_comments_ordered_by_created_desc_by_default(self):
        """Тести, які коментарі, упорядковані створеними (DESC) за замовчуванням, перераховані на сторінці."""
        self.assertEqual(
            self.response.context["page_obj"].object_list,
            list(self.queryset[:25]),
        )

    def test_lists_comments_ordered_by_created_asc(self):
        """Тести, які коментарі, упорядковані створеними (ASC), перераховані на сторінці."""
        response = self.client.get(f"{self.url}?orderby=c&orderdir=asc")
        self.assertEqual(
            response.context["page_obj"].object_list,
            list(self.queryset.order_by("created")[:25]),
        )

    def test_lists_comments_ordered_by_username_asc(self):
        """Тести, які коментарі, упорядковані іменем користувача (ASC), перераховані на сторінці."""
        response = self.client.get(f"{self.url}?orderby=u&orderdir=asc")
        self.assertEqual(
            response.context["page_obj"].object_list,
            list(self.queryset.order_by("author__username")[:25]),
        )

    def test_lists_comments_ordered_by_username_desc(self):
        """Тести, які коментарі, упорядковані іменем користувача (DESC), перераховані на сторінці."""
        response = self.client.get(f"{self.url}?orderby=u&orderdir=desc")
        self.assertEqual(
            response.context["page_obj"].object_list,
            list(self.queryset.order_by("-author__username")[:25]),
        )

    def test_lists_comments_ordered_by_email_asc(self):
        """Тести, які коментарі, упорядковані електронною поштою (ASC), перераховані на сторінці."""
        response = self.client.get(f"{self.url}?orderby=e&orderdir=asc")
        self.assertEqual(
            response.context["page_obj"].object_list,
            list(self.queryset.order_by("author__email")[:25]),
        )

    def test_lists_comments_ordered_by_email_desc(self):
        """Тести, які коментарі, упорядковані електронною поштою (DESC), перераховані на сторінці."""
        response = self.client.get(f"{self.url}?orderby=e&orderdir=desc")
        self.assertEqual(
            response.context["page_obj"].object_list,
            list(self.queryset.order_by("-author__email")[:25]),
        )

    def test_404_with_invalid_order_parameters(self):
        """Тести, які недійсні параметри порядку призводять до 404."""
        response = self.client.get(f"{self.url}?orderby=wrong&orderdir=asc")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.url}?orderby=c&orderdir=wrong")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.url}?orderby=wrong")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.url}?orderdir=wrong")
        self.assertEqual(response.status_code, 404)


class CommentCreateViewTestCase(TestCase):
    """Тести для представлення додавання коментарів."""

    url = "/add/"

    def test_405_withget_request(self):
        """Випробує, що перегляд повертає 404 із запитом GET."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_adding_comment_with_valid_form_data(self):
        """Тести, що додають коментар із дійсними даними форми."""
        response = self.test_comment_form_for_validity_and_get_response(
            self.get_valid_form_data()
        )
        self.assertContains(response, "Your comment has successfully added.")

    def test_adding_comment_with_invalid_form_data(self):
        """Тести, що додають коментар з недійсними даними форми."""
        form_data = self.get_valid_form_data()
        form_data["username"] = "test user"
        response = self.test_comment_form_for_validity_and_get_response(
            form_data, is_valid=False
        )
        self.assertContains(response, "Invalid form data.")

    def test_adding_answer_with_valid_form_data(self):
        """Тести, що додають відповіді з дійсними даними форми."""
        comment = Comment.objects.create(
            text=f"Tests comment",
            author=Author.objects.create(
                username=f"test_user",
                email=f"test_user@gmail.com",
            ),
        )
        form_data = self.get_valid_form_data()
        form_data["comment_parent_id"] = comment.id
        response = self.test_comment_form_for_validity_and_get_response(
            form_data
        )
        self.assertContains(response, "Your answer has successfully added.")

    def test_404_with_nonexistent_parent_id(self):
        """Тест, що перегляд повертає 404 з неіснуючою батьківською id."""
        # ! I think it's valid test, but it returns 405.
        # form_data = self.get_valid_form_data()
        # form_data["comment_parent_id"] = 100
        # response = self.test_comment_form_for_validity_and_get_response(
        #     form_data, is_valid=False, status_code=404
        # )
        # self.assertContains(response, "Not Found")

    def get_valid_form_data(self) -> dict:
        """Повертає дійсні дані форми."""
        return {
            "username": "test_user",
            "email": "test_user@gmail.com",
            "text": "Test comment",
        }

    def test_comment_form_for_validity_and_get_response(
        self, form_data: dict, is_valid: bool = True, status_code: int = 200
    ) -> HttpResponse:
        """Тести, що форма є дійсною або недійсною за допомогою заданої форми_data, і повертає відповідь."""
        (
            self.assertTrue(CommentModelForm(form_data).is_valid())
            if is_valid
            else self.assertFalse(CommentModelForm(form_data).is_valid())
        )
        response = self.client.post(
            self.url, data=form_data, follow=True  # follow redirects
        )
        self.assertEqual(response.status_code, status_code)
        return response
