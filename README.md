# Kittygram_plus

### Описание:
Проект илюстрирует возможности DRF.

В проекте описана простая модель базы котов, их достижений и их владельцев.
В проекте есть примеры реализации CRUD в виде view-функций, низкоуровневых view-classes, дженериков и вьюсетов.

### Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:akchau/kittygram_plus.git
```

```
cd kittygram_plus
```

2. Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

3. Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
