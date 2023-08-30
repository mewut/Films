from datetime import date
from django.db import models


class Category(models.Model):
    name = models.CharField('Категория', max_length=255)
    description = models.TextField('Описание', max_length=255)
    url = models.SlugField(max_length=155, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    name = models.CharField('Имя', max_length=255)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание', max_length=2255)
    image = models.ImageField('Изображение', upload_to='actors/')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Актеры и режиссеры'
        verbose_name_plural = 'Актеры и режиссеры'


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=255)
    description = models.TextField('Описание', max_length=255)
    url = models.SlugField(max_length=155, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    
class Movie(models.Model):
    title = models.CharField('Название', max_length=255)
    tagline = models.CharField('Слоган', max_length=255, default='')
    description = models.TextField('Описание', max_length=2255)
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Дата выхода', default='2000')
    country = models.CharField('Страна', max_length=155)                        # можно потом сделать список стран на выбор
    directors = models.ManyToManyField(Actor, verbose_name='режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='актеры', related_name='actors')
    genres = models.ManyToManyField(Genre, verbose_name='жанры')
    world_premiere = models.DateField('Премьера в мире', default=date.today)
    budget = models.PositiveIntegerField('Бюджет', default=0, help_text='в долларах')
    fees_in_usa = models.PositiveIntegerField('Сборы в США', default=0, help_text='в долларах')
    fees_in_world = models.PositiveIntegerField('Сборы в мире', default=0, help_text='в долларах')
    category = models.ForeignKey(Category, verbose_name='категория', on_delete=models.SET_NULL, null=True)   # почему SET_NULL, а не CASCADE: 
                                                                                        # если мы удалим категорию, в которой был этот фильм, 
                                                                                        # # то у фильма просто останется пустое поле. 
    url = models.SlugField(max_length=155, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    description = models.CharField('Описание', max_length=255)
    image = models.ImageField('Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='кадры из фильма', on_delete=models.CASCADE)    # при удалении фильма все кадры, связанные с ним, тоже удалятся

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField('Значение', default=0)

    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'


class Rating(models.Model):
    ip = models.CharField('IP-адрес', max_length=55)
    star = models.ForeignKey(RatingStar, verbose_name='звезда', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name='фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.star} - {self.movie}" 
    
    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField('Имя', max_length=25)
    text = models.TextField('Отзыв', max_length=5555)
    parent = models.ForeignKey('self', verbose_name='родитель', on_delete=models.SET_NULL, null=True, blank=True)
    movie = models.ForeignKey(Movie, verbose_name='фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}" 
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

