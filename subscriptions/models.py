from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from .constants import (
    LENGTH_LIMIT_DESCRIPTION_FIELD,
    LENGTH_LIMITS_CHAR_FIELDS,
    LENGTH_LIMITS_PRICE_FIELDS,
    LENGTH_LIMIT_ACCOUNT_FIELD,
    LENGTH_LIMIT_PHONE_NUMBER_FIELD,
    LENGTH_LIMITS_LINK_FIELDS,
    DECIMAL_PLACES,
    MIN_VALUE_DECIMAL_FIELDS,
    PROMOCODE_LENGHT,
    PROMOCODE_ERROR_MESSAGE,
    MONTH,
    UNDONE,
    SUBSCRIPTION_PERIOD,
    TRANSACTION_STATUS,
    USER,
    COVER,
    SUBSCRIPTION,
    USER_SUBSCRIPTION,
    TRANSACTION
)


class User(AbstractUser):
    """Модель пользователя."""
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']
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
        default=0,
        validators=(MinValueValidator(MIN_VALUE_DECIMAL_FIELDS),)
    )
    cashback = models.DecimalField(
        'Кэшбек',
        max_digits=LENGTH_LIMITS_PRICE_FIELDS,
        decimal_places=DECIMAL_PLACES,
        default=0,
        validators=(MinValueValidator(MIN_VALUE_DECIMAL_FIELDS),),
    )

    class Meta:
        ordering = ('phone_number',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return USER.format(
            phone_number=self.phone_number,
            account_balance=self.account_balance,
            cashback=self.cashback
        )


class Category(models.Model):
    """Модель категорий"""
    name = models.CharField(
        'Название',
        max_length=LENGTH_LIMITS_CHAR_FIELDS
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


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

    def __str__(self):
        return COVER.format(name=self.name, preview=self.preview)


class Subscription(models.Model):
    """Модель подписок"""
    name = models.CharField(
        'Название',
        max_length=LENGTH_LIMITS_CHAR_FIELDS
    )
    description = models.CharField(
        'Описание',
        max_length=LENGTH_LIMIT_DESCRIPTION_FIELD
    )

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
    users = models.ManyToManyField(
        User,
        through='Transaction',
        verbose_name='Пользователи'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return SUBSCRIPTION.format(
            name=self.name,
            description=self.description,
            monthly_price=self.monthly_price,
            semi_annual_price=self.semi_annual_price,
            annual_price=self.semi_annual_price
        )


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
        auto_now=False,
        auto_now_add=True,
        editable=True
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
    promocode = models.CharField(
        'Промокод',
        default='',
        max_length=PROMOCODE_LENGHT,
        validators=(RegexValidator(
            regex='^[A-Z0-9]+$', message=PROMOCODE_ERROR_MESSAGE
        ),),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-end_date', 'price')
        verbose_name = 'Пользователь/Подписка'
        verbose_name_plural = 'Пользователи/Подписки'
        constraints = [models.UniqueConstraint(
            fields=['user', 'subscription'],
            name='unique_user_subscription'
        )]

    def __str__(self):
        return USER_SUBSCRIPTION.format(
            user=self.user.phone_number,
            subscription=self.subscription.name,
            start_date=self.start_date,
            end_date=self.end_date,
            price=self.price,
            period=self.period,
            autorenewal=self.autorenewal
        )


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

    def __str__(self):
        return self.card_number


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        related_name='transactions',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Подписка'
    )
    amount = models.DecimalField(
        'Сумма',
        max_digits=LENGTH_LIMITS_PRICE_FIELDS,
        decimal_places=DECIMAL_PLACES,
        default=0.00,
        validators=(MinValueValidator(MIN_VALUE_DECIMAL_FIELDS),)
    )
    timestamp = models.DateTimeField(auto_now=True,)
    status = models.CharField(
        'Статус транзакции',
        max_length=max(len(status) for status, _ in TRANSACTION_STATUS),
        default=UNDONE,
        choices=TRANSACTION_STATUS)

    class Meta:
        ordering = ('timestamp',)
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return TRANSACTION.format(
            user=self.user.phone_number,
            subscription=self.subscription.name,
            amount=self.amount,
            timestamp=self.timestamp,
            status=self.status
        )
