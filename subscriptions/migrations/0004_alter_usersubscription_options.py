# Generated by Django 5.0.3 on 2024-03-28 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_alter_usersubscription_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usersubscription',
            options={'ordering': ('-end_date', 'price'), 'verbose_name': 'Пользователь/Подписка', 'verbose_name_plural': 'Пользователи/Подписки'},
        ),
    ]
