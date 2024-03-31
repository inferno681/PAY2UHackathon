import random
import string

from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont

from subscriptions.models import (
    Transaction,
    UserSubscription,
    DONE,
    PROMOCODE_LENGHT,
    UNDONE
)

PROMOCODE_SYMBOLS = string.ascii_uppercase + string.digits


def promocode_generator():
    while (True):
        promocode = ''.join(random.choices(PROMOCODE_SYMBOLS,
                                           k=PROMOCODE_LENGHT))
        if not UserSubscription.objects.filter(promocode=promocode).exists():
            break
    return promocode


def pdf_receipt_generator(id, phone_number, name, end_date, promocode, price):
    drawing_data = (
        f'Номер телефона: {phone_number}',
        f'Название: {name}',
        f'Действует до: {end_date}',
        f'Цена: {price}',
        f'Промокод: {promocode}'
    )
    pdfmetrics.registerFont(
        TTFont('timesnewromanpsmt', 'timesnewromanpsmt.ttf',))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ('attachment; '
                                       f'filename="Reciept#{id}.pdf"')
    page = canvas.Canvas(response)
    page.setFont('timesnewromanpsmt', size=16)
    page.drawString(250, 800, 'PAY2U')
    page.drawString(200, 750, 'Подписка оформлена')
    page.setFont('timesnewromanpsmt', size=14)
    height = 725
    for i in drawing_data:
        page.drawString(75, height, i)
        height -= 25
    page.showPage()
    page.save()
    return response


def payment(user, subscription, amount):
    status = UNDONE if user.account_balance < amount else DONE
    Transaction.objects.create(
        user=user,
        subscription=subscription,
        amount=amount,
        status=status
    )
    user.account_balance -= amount
    user.save()
    return True if status == DONE else False


def cashback_calculation(user, amount, cashback_percent):
    user.cashback += amount * (cashback_percent / 100)
    user.save()
