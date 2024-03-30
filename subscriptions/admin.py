from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils import timezone
from django.utils.safestring import mark_safe

from .models import (
    Category,
    Card,
    Cover,
    Subscription,
    User,
    UserSubscription,
)


admin.site.empty_value_display = 'Не задано'
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'email',
        'username',
        'is_staff',
        'first_name',
        'middle_name',
        'last_name',
        'phone_number',
        'account_balance',
        'cashback',
        'active_subscriptions_amount',
        'inactive_subscriptions_amount'

    )
    readonly_fields = (
        'active_subscriptions_amount',
        'inactive_subscriptions_amount',
    )
    search_fields = (
        'email',
        'username',
        'is_staff',
        'first_name',
        'middle_name',
        'last_name',
        'phone_number',
    )

    @display(description='Активных подписок')
    def active_subscriptions_amount(self, user):
        return user.usersubscriptions.filter(
            end_date__gte=timezone.now().date()
        ).count()

    @display(description='Неактивных подписок')
    def inactive_subscriptions_amount(self, user):
        return user.usersubscriptions.filter(
            end_date__lt=timezone.now().date()
        ).count()


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'start_date',
        'end_date',
        'price',
        'period',
        'promocode',
        'subscription_id',
        'user_id',
        'autorenewal'
    )

    search_fields = (
        'start_date',
        'end_date',
        'price',
        'period',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Cover)
class CoverAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'preview',
        'logo_link',
        'show_logo',
        'service_link',
        'show_categories',
    )
    list_filter = ('name', 'categories__name')
    search_fields = ('name', 'categories__name')
    readonly_fields = ('show_categories', 'show_logo')

    @display(description='Категории')
    @mark_safe
    def show_categories(self, cover):
        return '<br> '.join(
            cover.name
            for cover in cover.categories.all()
        )

    @display(description='Лого')
    @mark_safe
    def show_logo(self, cover):
        return f'<img src="{cover.logo_link}" width="50" height="50" />'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'monthly_price',
        'semi_annual_price',
        'annual_price',
        'cashback_percent',

    )
    list_filter = ('name', 'monthly_price', 'cashback_percent')
    search_fields = ('name',)


@admin.register(Card)
class CaedAdmin(admin.ModelAdmin):
    list_display = ('card_number',)
    list_filter = ('card_number',)
    search_fields = ('card_number',)
