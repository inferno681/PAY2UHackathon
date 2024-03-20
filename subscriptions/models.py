from django.db import models


class Subscriptions(models.Model):
    name = models.CharField('Название', max_lemax_length=150)
    description = models.TextField('Описание')
    monthly_price = models.FloatField(
        'Цена подписки за месяц', decimal_places=2)
    semi_annual_price = models.FloatField(
        'Цена подписки за полгода', decimal_places=2)
    annual_price = models.FloatField('Цена подписки за год', decimal_places=2)
    users = models.ManyToManyField(
        User,
        through='UserSubscription',
        verbose_name='Пользователи'
    )
