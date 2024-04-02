from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from sms import send_sms

from api.functions import cashback_calculation, payment
from api.serializers import ADDITION_SUBSCRIPTION_DAYS, INSUFFICIENT_FUNDS
from subscriptions.models import User, UserSubscription

AUTOPAYMENT_REPORT = 'Prolongations for {count} clients done'
CASHBACK_CREDIT_REPORT = 'Cashback crediting for {count} clients done'
SEND_SMS_REPORT = 'Sent to {country_code}{recipient}'


@shared_task
def autopayment():
    count = 0
    for usersubscription in UserSubscription.objects.all():
        if usersubscription.end_date == timezone.now().date(
        ) and usersubscription.autorenewal:
            if not payment(
                usersubscription.user,
                usersubscription.subscription,
                usersubscription.price
            ):
                return INSUFFICIENT_FUNDS
            cashback_calculation(
                usersubscription.user,
                usersubscription.price,
                usersubscription.subscription.cashback_percent
            )
            usersubscription.end_date += timedelta(
                days=ADDITION_SUBSCRIPTION_DAYS[usersubscription.period])
            usersubscription.save()
            count += 1
    return AUTOPAYMENT_REPORT.format(count=count)


@shared_task
def cashback_credit():
    count = 0
    for user in User.objects.all():
        if user.usersubscription.start_date.first() == timezone.now().date():
            user.account_balance += user.cashback
            user.cashback = 0
            user.save()
            count += 1

    return CASHBACK_CREDIT_REPORT.format(count=count)


@shared_task
def send_sms_task(text, sender, recipient, country_code='+7'):
    send_sms(
        text,
        sender,
        [country_code + recipient],
        fail_silently=False
    )
    return SEND_SMS_REPORT(country_code=country_code, recipient=recipient)
