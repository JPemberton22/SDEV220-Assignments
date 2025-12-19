# this is the code that I used following the tutorial for Django installation - Django admin

mkdir djangogirls
cd djangogirls
python -m venv myvenv
myvenv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
django-admin.exe startproject mysite .


TIME_ZONE = 'America/Indiana/Indianapolis'
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.pythonanywhere.com']


python manage.py migrate
python manage.py runserver


python manage.py startapp blog


from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


python manage.py makemigrations blog
python manage.py migrate blog


from django.contrib import admin
from .models import Post

admin.site.register(Post)


python manage.py runserver
python manage.py createsuperuser
