from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch

from subscriptions import MONTH
from subscriptions.models import (
    Category,
    Cover,
    Subscription,
    UserSubscription
)
User = get_user_model()

"""Адреса"""
CATEGORY_LIST_NAME = 'category-list'
CATEGORY_DETAIL_NAME = 'category-detail'
COVER_LIST_NAME = 'cover-list'
COVER_DETAIL_NAME = 'cover-detail'
USER_NAME = 'my'
SUBSCRIPTION_CREATE_NAME = 'subscription-list'
SUBSCRIPTION_DETAIL_NAME = 'subscription-detail'
SUBSCRIPTION_GET_REPORT_NAME = 'subscription-get-reciept'

"""Запросы"""
SUBSCRIPTION_CREATE_DATA = {
    'id': 3,
    'period': MONTH,
    'autorenewal': True
}
SUBSCRIPTION_UPDATE_DATA = {
    'period': MONTH,
    'autorenewal': True
}

"""Ответы"""
COVER_LIST_RESULT = {
    'count': 3,
    'next': None,
    'previous': None,
    'results': [
        {
            'id': 1,
            'name': 'cover_name_1',
            'preview': 'preview',
            'logo_link': 'logo_link',
            'price': '10',
            'cashback_percent': '10',
            'categories': [
                1
            ],
            'is_subscribed': True
        },
        {
            'id': 2,
            'name': 'cover_name_2',
            'preview': 'preview',
            'logo_link': 'logo_link',
            'price': '10',
            'cashback_percent': '10',
            'categories': [
            ],
            'is_subscribed': False
        },
        {
            'id': 3,
            'name': 'cover_name_3',
            'preview': 'preview',
            'logo_link': 'logo_link',
            'price': '10',
            'cashback_percent': '10',
            'categories': [
            ],
            'is_subscribed': False
        }
    ]
}
COVER_DETAIL_RESULT = {
    'name': 'cover_name_1',
    'logo_link': 'logo_link',
    'service_link': 'service_link',
    'categories': [
        1
    ],
    'subscriptions': [
        {
            'id': 1,
            'is_subscribed': True,
            'end_date': str(timezone.now().date() + timedelta(days=15)),
            'name': 'active_subscription',
            'description': 'description',
            'monthly_price': '10.00',
            'semi_annual_price': '50.00',
            'annual_price': '95.00',
            'cashback_percent': '10.00',
            'cover': 1
        }
    ]
}
MY_RESULT = {
    'phone_number': '777',
    'first_name': '',
    'middle_name': '',
    'last_name': '',
    'account_balance': '5000.00',
    'cashback': '0.00',
    'subscriptions': [
        {
            'id': 1,
            'name': 'active_subscription',
            'description': 'description',
            'end_date': str(timezone.now().date() + timedelta(days=15)),
            'price': '10.00',
            'period': MONTH,
            'logo_link': 'logo_link',
            'categories': [
                1
            ],
            'autorenewal': True,
            'promocode': 'promocode1',
            'is_active': True
        },
        {
            'id': 2,
            'name': 'inactive_subscription',
            'description': 'description',
            'end_date': str(timezone.now().date() - timedelta(days=15)),
            'price': '10.00',
            'period': MONTH,
            'logo_link': 'logo_link',
            'categories': [
            ],
            'autorenewal': True,
            'promocode': 'promocode2',
            'is_active': False
        }
    ],
    'current_month_expenses': None
}
SUBSCRIPTION_CREATE_RESULT = {
    'id': 3,
    'is_subscribed': True,
    'end_date': str(timezone.now().date() + timedelta(days=30)),
    'logo_link': 'logo_link',
    'service_link': 'service_link',
    'categories': [
    ],
    'period': MONTH,
    'autorenewal': True,
    'promocode': 'promocode1',
    'cover_name': 'cover_name_3',
    'name': 'new_subscription',
    'description': 'description',
    'monthly_price': '10.00',
    'semi_annual_price': '50.00',
    'annual_price': '95.00',
    'cashback_percent': '10.00',
    'cover': 3
}
SUBSCRIPTION_UPDATE_RESULT = {
    'id': 2,
    'is_subscribed': True,
    'end_date': str(timezone.now().date() + timedelta(days=30)),
    'logo_link': 'logo_link',
    'service_link': 'service_link',
    'categories': [
    ],
    'period': MONTH,
    'autorenewal': True,
    'promocode': 'promocode1',
    'cover_name': 'cover_name_2',
    'name': 'inactive_subscription',
    'description': 'description',
    'monthly_price': '10.00',
    'semi_annual_price': '50.00',
    'annual_price': '95.00',
    'cashback_percent': '10.00',
    'cover': 2
}

SUBSCRIPTION_DETAIL_RESULT = {
    'id': 1,
    'is_subscribed': True,
    'end_date': str(timezone.now().date() + timedelta(days=15)),
    'logo_link': 'logo_link',
    'service_link': 'service_link',
    'categories': [
        1
    ],
    'period': MONTH,
    'autorenewal': True,
    'promocode': 'promocode1',
    'cover_name': 'cover_name_1',
    'name': 'active_subscription',
    'description': 'description',
    'monthly_price': '10.00',
    'semi_annual_price': '50.00',
    'annual_price': '95.00',
    'cashback_percent': '10.00',
    'cover': 1
}


class APITest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create(
            username='user',
            phone_number='777',
            password='mypass',
            account_balance=5000
        )
        cls.client = APIClient()
        cls.token = str(RefreshToken.for_user(cls.user).access_token)
        cls.category = Category.objects.create(name='category')
        cls.cover_1 = Cover.objects.create(
            name='cover_name_1',
            preview='preview',
            logo_link='logo_link',
            service_link='service_link',
        )
        cls.cover_2 = Cover.objects.create(
            name='cover_name_2',
            preview='preview',
            logo_link='logo_link',
            service_link='service_link',
        )
        cls.cover_3 = Cover.objects.create(
            name='cover_name_3',
            preview='preview',
            logo_link='logo_link',
            service_link='service_link',
        )
        cls.cover_1.categories.add(cls.category)
        cls.active_subscription = Subscription.objects.create(
            name='active_subscription',
            description='description',
            monthly_price=10,
            semi_annual_price=50,
            annual_price=95,
            cashback_percent=10,
            cover=cls.cover_1
        )
        cls.inactive_subscription = Subscription.objects.create(
            name='inactive_subscription',
            description='description',
            monthly_price=10,
            semi_annual_price=50,
            annual_price=95,
            cashback_percent=10,
            cover=cls.cover_2
        )
        cls.new_subscription = Subscription.objects.create(
            name='new_subscription',
            description='description',
            monthly_price=10,
            semi_annual_price=50,
            annual_price=95,
            cashback_percent=10,
            cover=cls.cover_3
        )
        UserSubscription.objects.create(
            user=cls.user,
            subscription=cls.active_subscription,
            start_date=timezone.now().date() - timedelta(days=33),
            end_date=timezone.now().date() + timedelta(days=15),
            price=cls.active_subscription.monthly_price,
            period=MONTH,
            autorenewal=True,
            promocode='promocode1'
        )
        UserSubscription.objects.create(
            user=cls.user,
            subscription=cls.inactive_subscription,
            start_date=timezone.now().date() - timedelta(days=33),
            end_date=timezone.now().date() - timedelta(days=15),
            price=cls.active_subscription.monthly_price,
            period=MONTH,
            autorenewal=True,
            promocode='promocode2'
        )

    def test_receive_token(self):
        response = self.client.post(
            '/api/auth/token/', data={'phone_number': self.user.phone_number})
        self.assertEqual(response.status_code, 200)
        token = str(RefreshToken.for_user(self.user).access_token)
        self.assertEqual(len(token), len(response.data['token']))

    def test_get_categories_list(self):
        response = self.client.get(
            reverse(CATEGORY_LIST_NAME),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{'id': 1, 'name': 'category'}])

    def test_get_category_detail(self):
        response = self.client.get(
            reverse(CATEGORY_DETAIL_NAME, kwargs={'pk': self.category.pk}),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'id': 1, 'name': 'category'})

    def test_get_covers_list(self):
        response = self.client.get(
            reverse(COVER_LIST_NAME),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, COVER_LIST_RESULT)

    def test_get_cover_detail(self):
        response = self.client.get(
            reverse(COVER_DETAIL_NAME, kwargs={'pk': self.cover_1.pk}),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, COVER_DETAIL_RESULT)

    def test_get_user_info(self):
        response = self.client.get(
            reverse(USER_NAME),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, MY_RESULT)

    def test_subscribe_new_subscription(self):
        with patch('api.tasks.send_sms_task.delay') as mock_apply_async:
            response = self.client.post(
                reverse(SUBSCRIPTION_CREATE_NAME),
                data=SUBSCRIPTION_CREATE_DATA,
                headers={'Authorization': f'Bearer {self.token}'}
            )
            mock_apply_async.assert_called_once
            SUBSCRIPTION_CREATE_RESULT[
                'promocode'
            ] = UserSubscription.objects.get(
                subscription=self.new_subscription).promocode
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data, SUBSCRIPTION_CREATE_RESULT)

    def test_subscribe_old_subscription(self):
        with patch('api.tasks.send_sms_task.delay') as mock_apply_async:
            response = self.client.patch(
                reverse(SUBSCRIPTION_DETAIL_NAME,
                        kwargs={'pk': self.inactive_subscription.pk}),
                data=SUBSCRIPTION_UPDATE_DATA,
                headers={'Authorization': f'Bearer {self.token}'}
            )
            mock_apply_async.assert_called_once
            SUBSCRIPTION_UPDATE_RESULT[
                'promocode'
            ] = UserSubscription.objects.get(
                subscription=self.inactive_subscription).promocode
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, SUBSCRIPTION_UPDATE_RESULT)

    def test_get_subscription_detail(self):
        response = self.client.get(
            reverse(SUBSCRIPTION_DETAIL_NAME, kwargs={
                    'pk': self.active_subscription.pk}),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, SUBSCRIPTION_DETAIL_RESULT)

    def test_get_reciept(self):
        response = self.client.get(
            reverse(SUBSCRIPTION_GET_REPORT_NAME, kwargs={
                    'pk': self.active_subscription.pk}),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/pdf')
        self.assertIn('attachment', response['content-disposition'])
        self.assertIn(
            f'Reciept#{self.active_subscription.id}.pdf',
            response['content-disposition']
        )
