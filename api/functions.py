import random
import string

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A5
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from subscriptions.models import UserSubscription, PROMOCODE_LENGHT

PROMOCODE_SYMBOLS = string.ascii_uppercase + string.digits


def promocode_generator():
    while (True):
        promocode = ''.join(random.choices(PROMOCODE_SYMBOLS,
                                           k=PROMOCODE_LENGHT))
        if not UserSubscription.objects.filter(promocode=promocode).exists():
            break
    return promocode


def pdf_receipt_generator(phone_number, name, end_date, promocode, price):

    pdfmetrics.registerFont(
        TTFont('timesnewromanpsmt', 'timesnewromanpsmt.ttf',))
    styles = getSampleStyleSheet()
    heading = styles['Title']
    heading.fontName = 'timesnewromanpsmt'
    heading.fontSize = 14
    body = styles['BodyText']
    body.fontName = 'timesnewromanpsmt'
    body.fontSize = 12
    heading_text = ('PAY2U <br/>'
                    'Подписка оформлена<br/><br/>')
    body_text = (
        f'Номер телефона: {phone_number} <br/><br/>'
        f'Название: {name} <br/><br/>'
        f'Действует до: {end_date} <br/><br/>'
        f'Промокод: {promocode} <br/><br/>'
        f'Цена: {price}'
    )
    heading_para = Paragraph(heading_text, heading)
    body_para = Paragraph(body_text, body)
    elements = [heading_para, body_para]
    doc = SimpleDocTemplate('simple_pdf.pdf', pagesize=A5)
    doc.build(elements)
