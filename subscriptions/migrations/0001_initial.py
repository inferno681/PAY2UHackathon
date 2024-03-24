# Generated by Django 5.0.3 on 2024-03-23 18:23

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('logo_link', models.CharField(max_length=200, verbose_name='Ссылка на логотип')),
                ('service_link', models.CharField(max_length=200, verbose_name='Ссылка на сайт подписки')),
                ('monthly_price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена подписки за месяц')),
                ('semi_annual_price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена подписки за полгода')),
                ('annual_price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена подписки за год')),
                ('conditions', models.TextField(verbose_name='Условия')),
                ('cashback_procent', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='% кэшбека')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(max_length=10, unique=True, verbose_name='Номер телефона')),
                ('first_name', models.CharField(max_length=150, verbose_name='Имя')),
                ('middle_name', models.CharField(blank=True, max_length=150, verbose_name='Отчество')),
                ('last_name', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('account_balance', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Счет')),
                ('cashback', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Кэшбек')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('phone_number',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=19, unique=True, verbose_name='Номер карты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Банковская карта',
                'verbose_name_plural': 'Банковские карты',
                'ordering': ('card_number',),
            },
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now=True, verbose_name='Дата начала подписки')),
                ('end_date', models.DateField(blank=True, verbose_name='Дата окончания подписки')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Стоимость подписки')),
                ('period', models.CharField(choices=[('monthly', 'Месяц'), ('semi-annual', 'Полгода'), ('annual', 'Год')], default='monthly', max_length=11, verbose_name='Продолжительность подписки')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usersubscriptions', to='subscriptions.subscription', verbose_name='Подписка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usersubscriptions', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Пользователь/Подписка',
                'verbose_name_plural': 'Пользователи/Подписки',
                'ordering': ('user',),
            },
        ),
        migrations.AddField(
            model_name='subscription',
            name='users',
            field=models.ManyToManyField(through='subscriptions.UserSubscription', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи'),
        ),
        migrations.AddConstraint(
            model_name='usersubscription',
            constraint=models.UniqueConstraint(fields=('user', 'subscription'), name='unique_user_subscription'),
        ),
    ]
