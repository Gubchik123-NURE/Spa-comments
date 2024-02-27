"""Цей модуль використовується для розгортання проекту на сервері.

Цей модуль містить WSGI-сервер для розгортання проекту на сервері. 
WSGI (Web Server Gateway Interface) - це стандартний інтерфейс між веб-серверами і веб-додатками для Python. 
WSGI-сервер відповідає за обробку запитів, які надходять на сервер, і передачу їх веб-додатку для обробки.
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spa.settings")

application = get_wsgi_application()
