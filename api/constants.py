import string

from subscriptions import (
    ANNUAL,
    MONTH,
    SEMI_ANNUAL,
)

"""Константа для расчета продления подписки"""
ADDITION_SUBSCRIPTION_DAYS = {
    MONTH: 30,
    SEMI_ANNUAL: 180,
    ANNUAL: 365
}

"""Текст сообщений"""
SMS_TEXT = (
    'Вам оформлена подписка: '
    'Название: {name} '
    'Цена: {price} '
    'Описание: {description:.50} '
    'Промокод: {promocode}'
)
PAY2U_PHONE_NUMBER = '+70123456789'

"""Сообщения об ошибках"""
SUBSCRIPTION_EXIST_ERROR = {'error': 'Вы уже подписаные на один из тарифов'}
INSUFFICIENT_FUNDS = {'error': 'Недостаточно средств на счете'}
NO_DATA_TRANSFERED = {'error': 'Данные не переданы'}

"""Набор символов для генерации промокода"""
PROMOCODE_SYMBOLS = string.ascii_uppercase + string.digits

"""Сообщения о выполнении задач celery"""
AUTOPAYMENT_REPORT = 'Prolongations for {count} clients done'
CASHBACK_CREDIT_REPORT = 'Cashback crediting for {count} clients done'
SEND_SMS_REPORT = 'Sent to {country_code}{recipient}'
