::: comments.urls

```python
urlpatterns = [
    path("", views.CommentListView.as_view(), name="list"),
    path("add/", views.CommentCreateView.as_view(), name="add"),
]
```