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

CATEGORY_LIST_NAME = 'category-list'
CATEGORY_DETAIL_NAME = 'category-detail'
COVER_LIST_NAME = 'cover-list'
COVER_DETAIL_NAME = 'cover-detail'
USER_NAME = 'my'
SUBSCRIPTION_CREATE_NAME = 'subscription-list'
SUBSCRIPTION_DETAIL_NAME = 'subscription-detail'
SUBSCRIPTION_GET_REPORT_NAME = 'subscription-get-reciept'
SUBSCRIPTION_CREATE_DATA = {
    'id': 2,
    'period': MONTH,
    'autorenewal': True
}
COVER_LIST_RESULT = {
    'count': 1,
    'next': None,
    'previous': None,
    'results': [
        {
            'id': 1,
            'name': 'cover_name',
            'preview': 'preview',
            'logo_link': 'logo_link',
            'price': 10.00,
            'cashback_percent': 10.00,
            'categories': [
                1
            ],
            'is_subscribed': False
        }
    ]
}
COVER_DETAIL_RESULT = {
    'name': 'cover_name',
    'logo_link': 'logo_link',
    'service_link': 'service_link',
    'categories': [
        1
    ],
    'subscriptions': [
        {
            'id': 1,
            'is_subscribed': False,
            'end_date': None,
            'name': 'subscription_name',
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
    'account_balance': '0.00',
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
            'promocode': 'promocode2',
            'is_active': False
        }
    ],
    'current_month_expenses': None
}
SUBSCRIPTION_CREATE_RESULT = {
    'id': 2,
    'is_subscribed': True,
    'end_date': str(timezone.now().date() + timedelta(days=30)),
    'logo_link': 'logo_link',
    'service_link': 'service_link',
    'categories': [
        1
    ],
    'period': MONTH,
    'autorenewal': True,
    'promocode': 'promocode1',
    'name': 'subscription_second',
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
    'name': 'subscription_first',
    'description': 'description',
    'monthly_price': '10.00',
    'semi_annual_price': '50.00',
    'annual_price': '95.00',
    'cashback_percent': '10.00',
    'cover': 1
}


class GetTokenViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create(
            username='user', phone_number='777', password='mypass')
        cls.client = APIClient()

    def test_post(self):
        response = self.client.post(
            '/api/auth/token/', data={'phone_number': self.user.phone_number})
        self.assertEqual(response.status_code, 200)
        token = str(RefreshToken.for_user(self.user).access_token)
        self.assertEqual(len(token), len(response.data['token']))


class CategoryViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='user', phone_number='777', password='mypass')
        cls.client = APIClient()
        cls.token = str(RefreshToken.for_user(cls.user).access_token)
        cls.category = Category.objects.create(name='category')

    def test_get_list(self):
        response = self.client.get(
            reverse(CATEGORY_LIST_NAME),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{'id': 1, 'name': 'category'}])

    def test_get_detail(self):
        response = self.client.get(
            reverse(CATEGORY_DETAIL_NAME, kwargs={'pk': self.category.pk}),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'id': 1, 'name': 'category'})


class CoverViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='user', phone_number='777', password='mypass')
        cls.client = APIClient()
        cls.token = str(RefreshToken.for_user(cls.user).access_token)
        cls.category = Category.objects.create(name='category')
        cls.cover = Cover.objects.create(
            name='cover_name',
            preview='preview',
            logo_link='logo_link',
            service_link='service_link',
        )
        cls.cover.categories.add(cls.category)
        cls.subscription = Subscription.objects.create(
            name='subscription_name',
            description='description',
            monthly_price=10,
            semi_annual_price=50,
            annual_price=95,
            cashback_percent=10,
            cover=cls.cover
        )

    def test_get_list(self):
        response = self.client.get(
            reverse(COVER_LIST_NAME),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, COVER_LIST_RESULT)

    def test_get_detail(self):
        response = self.client.get(
            reverse(COVER_DETAIL_NAME, kwargs={'pk': self.cover.pk}),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, COVER_DETAIL_RESULT)


class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='user', phone_number='777', password='mypass')
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

    def test_get(self):
        response = self.client.get(
            reverse(USER_NAME),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, MY_RESULT)


class SubscriptionViewSetTest(APITestCase):
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
        cls.cover_1.categories.add(cls.category)
        cls.cover_2.categories.add(cls.category)
        cls.subscription_1 = Subscription.objects.create(
            name='subscription_first',
            description='description',
            monthly_price=10,
            semi_annual_price=50,
            annual_price=95,
            cashback_percent=10,
            cover=cls.cover_1
        )
        cls.subscription_2 = Subscription.objects.create(
            name='subscription_second',
            description='description',
            monthly_price=10,
            semi_annual_price=50,
            annual_price=95,
            cashback_percent=10,
            cover=cls.cover_2
        )
        UserSubscription.objects.create(
            user=cls.user,
            subscription=cls.subscription_1,
            start_date=timezone.now().date() - timedelta(days=33),
            end_date=timezone.now().date() + timedelta(days=15),
            price=cls.subscription_1.monthly_price,
            period=MONTH,
            autorenewal=True,
            promocode='promocode1'
        )

    def test_post(self):
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
                subscription=self.subscription_2).promocode
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data, SUBSCRIPTION_CREATE_RESULT)

    def test_get_detail(self):
        response = self.client.get(
            reverse(SUBSCRIPTION_DETAIL_NAME, kwargs={
                    'pk': self.subscription_1.pk}),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, SUBSCRIPTION_DETAIL_RESULT)

    def test_get_reciept(self):
        response = self.client.get(
            reverse(SUBSCRIPTION_GET_REPORT_NAME, kwargs={
                    'pk': self.subscription_1.pk}),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/pdf')
        self.assertIn('attachment', response['content-disposition'])
        self.assertIn(
            f'Reciept#{self.subscription_1.id}.pdf',
            response['content-disposition']
        )
