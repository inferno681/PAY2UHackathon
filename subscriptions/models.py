from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


LENGTH_LIMITS_CHAR_FIELDS = 150
LENGTH_LIMITS_PRICE_FIELDS = 7
LENGTH_LIMIT_ACCOUNT_FIELD = 10
LENGTH_LIMIT_PHONE_NUMBER_FIELD = 10
LENGTH_LIMITS_LINK_FIELDS = 200
DECIMAL_PLACES = 2
MIN_VALUE_DECIMAL_FIELDS = Decimal.from_float(0.0)

MONTH = 'monthly'
SEMI_ANNUAL = 'semi-annual'
ANNUAL = 'annual'

SUBSCRIPTION_PERIOD = (
    (MONTH, 'Месяц'),
    (SEMI_ANNUAL, 'Полгода'),
    (ANNUAL, 'Год')
)


class User(AbstractUser):
    """Модель пользователя."""
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    phone_number = models.CharField(
        'Номер телефона',
        max_length=LENGTH_LIMIT_PHONE_NUMBER_FIELD,
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=LENGTH_LIMITS_CHAR_FIELDS,
    )
    middle_name = models.CharField(
        'Отчество',
        max_length=LENGTH_LIMITS_CHAR_FIELDS,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=LENGTH_LIMITS_CHAR_FIELDS,
    )
    account_balance = models.DecimalField(
        'Счет',
        max_digits=LENGTH_LIMIT_ACCOUNT_FIELD,
        decimal_places=DECIMAL_PLACES,
        validators=(MinValueValidator(MIN_VALUE_DECIMAL_FIELDS),)
    )
    cashback = models.DecimalField(
        'Кэшбек',
        max_digits=LENGTH_LIMITS_PRICE_FIELDS,
        decimal_places=DECIMAL_PLACES,
        validators=(MinValueValidator(MIN_VALUE_DECIMAL_FIELDS),),
    )

    class Meta:
        ordering = ('phone_number',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=LENGTH_LIMITS_CHAR_FIELDS
    )


class Cover(models.Model):
    """Модель обложек для подписок"""
    name = models.CharField(
        'Название',
        max_length=LENGTH_LIMITS_CHAR_FIELDS
    )
    preview = models.TextField('Краткое описание')
    logo_link = models.CharField(
        'Ссылка на логотип',
        max_length=LENGTH_LIMITS_LINK_FIELDS,
    )
    service_link = models.CharField(
        'Ссылка на сайт подписки',
        max_length=LENGTH_LIMITS_LINK_FIELDS,
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Обложка'
        verbose_name_plural = 'Обложки'


class Subscription(models.Model):
    """Модель подписок"""
    name = models.CharField(
        'Название',
        max_length=LENGTH_LIMITS_CHAR_FIELDS
    )
    description = models.TextField('Описание')

    monthly_price = models.DecimalField(
        'Цена подписки за месяц',
        max_digits=LENGTH_LIMITS_PRICE_FIELDS,
        decimal_places=DECIMAL_PLACES,
        validators=(MinValueValidator(MIN_VALUE_DECIMAL_FIELDS),)
    )
    semi_annual_price = models.DecimalField(
        'Цена подписки за полгода',
        max_digits=LENGTH_LIMITS_PRICE_FIELDS,
        decimal_places=DECIMAL_PLACES,
        validators=(MinValueValidator(MIN_VALUE_DECIMAL_FIELDS),)
    )
    annual_price = models.DecimalField(
        'Цена подписки за год',
        max_digits=LENGTH_LIMITS_PRICE_FIELDS,
        decimal_places=DECIMAL_PLACES,
        validators=(MinValueValidator(MIN_VALUE_DECIMAL_FIELDS),)
    )
    cashback_percent = models.DecimalField(
        '% кэшбека',
        max_digits=5,
        decimal_places=DECIMAL_PLACES,
        validators=(MinValueValidator(MIN_VALUE_DECIMAL_FIELDS),)
    )
    users = models.ManyToManyField(
        User,
        through='UserSubscription',
        verbose_name='Пользователи'
    )
    cover = models.ForeignKey(
        Cover,
        related_name='subscriptions',
        on_delete=models.CASCADE,
        verbose_name='Обложка',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class UserSubscription(models.Model):
    """Модель связи M2M"""
    user = models.ForeignKey(
        User,
        related_name='usersubscriptions',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='usersubscriptions',
        verbose_name='Подписка'
    )
    start_date = models.DateField(
        'Дата начала подписки',
        auto_now=True,
        auto_now_add=False
    )
    end_date = models.DateField(
        'Дата окончания подписки',
        blank=True
    )
    price = models.DecimalField(
        'Стоимость подписки',
        max_digits=LENGTH_LIMITS_PRICE_FIELDS,
        decimal_places=DECIMAL_PLACES,
        validators=(MinValueValidator(MIN_VALUE_DECIMAL_FIELDS),)
    )
    period = models.CharField(
        'Продолжительность подписки',
        max_length=max(len(period) for period, _ in SUBSCRIPTION_PERIOD),
        default=MONTH,
        choices=SUBSCRIPTION_PERIOD
    )
    autorenewal = models.BooleanField(
        'Автопродление',
        default=True
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Пользователь/Подписка'
        verbose_name_plural = 'Пользователи/Подписки'
        constraints = [models.UniqueConstraint(
            fields=['user', 'subscription'],
            name='unique_user_subscription'
        )]


class Card(models.Model):
    user = models.ForeignKey(
        User,
        related_name='cards',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    card_number = models.CharField(
        'Номер карты',
        max_length=19,
        unique=True
    )

    class Meta:
        ordering = ('card_number',)
        verbose_name = 'Банковская карта'
        verbose_name_plural = 'Банковские карты'
