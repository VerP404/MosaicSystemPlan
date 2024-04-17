FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV DJANGO_SUPERUSER_USERNAME admin
ENV DJANGO_SUPERUSER_PASSWORD admin
ENV DJANGO_SUPERUSER_EMAIL admin@example.com
ENV TZ=Europe/Moscow

WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code/

# Копируем .env файл в контейнер
COPY .env.dev .env

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Команда для запуска приложения
CMD python manage.py migrate \
    && python manage.py collectstatic --no-input \
#    && python manage.py createsuperuser --username admin --email admin@example.com --no-input\
     && python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('rdn', 'admin@example.com', 'rdn') if not User.objects.filter(username='rdn').exists() else None" \
#    && python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user('admin', password='Qaz123') if not User.objects.filter(username='admin').exists() else None" \
    && exec python manage.py runserver 0.0.0.0:8000
