::: spa.urls

```python
handler400 = CustomBadRequestView.as_view()
handler404 = CustomNotFoundView.as_view()

urlpatterns = [
    path("captcha/", include("captcha.urls")),
    path("", include("comments.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```