from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from .validators import validate_year


class Category(models.Model):
    """
    Модель категорий произведений.
    """
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Имя',
        db_index=True
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """
    Модель жанров произведений.
    """
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Имя',
        db_index=True
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """
    Модель произведений.
    """
    name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        db_index=True
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year],
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория',
        db_index=True
    )
    description = models.TextField(
        verbose_name='Краткое описание')
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанры',
        db_index=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    """
    Модель для ManyToMany связи между произведенями и жанрами.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    def __str__(self):
        return f'{self.title} : {self.genre}'

    class Meta:
        verbose_name = 'Связь жанра и произведения'
        verbose_name_plural = 'Связи жанров и произведений'


class Review(models.Model):
    """
    Модель для отзывов к произведенияем.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        db_index=True
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        default=1,
        verbose_name='Оценка',
        validators=[
            MaxValueValidator(10, 'Максимальная оценка - 10'),
            MinValueValidator(1, 'Минимальная оценка - 1'),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        # только один отзыв на каждое произведение для одного автора
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:10]
