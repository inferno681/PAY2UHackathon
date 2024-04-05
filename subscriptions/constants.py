from decimal import Decimal

"""Ограничения полей моделий"""
LENGTH_LIMIT_DESCRIPTION_FIELD = 28
LENGTH_LIMIT_PREVIEW_FIELD = 24
LENGTH_LIMITS_CHAR_FIELDS = 150
LENGTH_LIMITS_PRICE_FIELDS = 7
LENGTH_LIMIT_ACCOUNT_FIELD = 10
LENGTH_LIMIT_PHONE_NUMBER_FIELD = 10
LENGTH_LIMITS_LINK_FIELDS = 200
DECIMAL_PLACES = 2
MIN_VALUE_DECIMAL_FIELDS = Decimal.from_float(0.0)
PROMOCODE_LENGHT = 13

"""Сообщения об ошибках"""
PROMOCODE_ERROR_MESSAGE = 'Промокод содержит недопустимые символы'

"""Наполнение полей с выбором"""
MONTH = 'monthly'
SEMI_ANNUAL = 'semi-annual'
ANNUAL = 'annual'
DONE = 'done'
UNDONE = 'undone'

SUBSCRIPTION_PERIOD = (
    (MONTH, 'Месяц'),
    (SEMI_ANNUAL, 'Полгода'),
    (ANNUAL, 'Год')
)

TRANSACTION_STATUS = {
    (DONE, 'Выполнена'),
    (UNDONE, 'Не выполнена'),
}

"""__str__ моделей"""
USER = (
    'Номер телефона: {phone_number}. '
    'Баланс: {account_balance}. '
    'Кэшбек: {cashback}.'
)

COVER = (
    'Название: {name:.15}. '
    'Описание: {preview:.30}.'
)
SUBSCRIPTION = (
    'Название: {name:.15}. '
    'Описание: {description:.30}. '
    'Цена за месяц: {monthly_price}. '
    'Цена за полгода: {semi_annual_price}. '
    'Цена за год: {annual_price}.'
)

USER_SUBSCRIPTION = (
    'Пользователь: {user} '
    'Подписка: {subscription:.15} '
    'Дата начала: {start_date} '
    'Дата окончания: {end_date} '
    'Цена: {price} '
    'Период: {period} '
    'Автопродление: {autorenewal} '
)

TRANSACTION = (
    'Пользователь: {user} '
    'Подписка: {subscription:.15} '
    'Сумма: {amount} '
    'Время: {timestamp} '
    'Статус: {status} '
)
