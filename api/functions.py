import random
import string

from subscriptions.models import UserSubscription, PROMOCODE_LENGHT

PROMOCODE_SYMBOLS = string.ascii_uppercase + string.digits


def promocode_generator():
    while (True):
        promocode = ''.join(random.choices(PROMOCODE_SYMBOLS,
                                           k=PROMOCODE_LENGHT))
        if not UserSubscription.objects.filter(promocode=promocode).exists():
            break
    return promocode
