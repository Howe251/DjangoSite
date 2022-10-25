# DjangoSite
Репозиторий для сайта по фильмам, отсканированным в репозитории site

## Перед запуском
**1)** Создать secrets.py рядом с settings.py

**2)** Вставить 
```
SECRET_KEY = "Любые рандомные английские и спец символы"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Имя базы данных',
        'USER': 'Имя пользователя',
        'PASSWORD': 'Пароль',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

XAPIKEY = "Ключ к API KinopoiskApiUnofficial"
```
<sub>Ключ можно получить [здесь](https://kinopoiskapiunofficial.tech/documentation/api/) </sub>

**3)** Выполнить 
```
python manage.py makemigrations
python manage.py migrate
```