# Generated by Django 5.0.3 on 2024-03-27 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='autorenewal',
            field=models.BooleanField(default=True, verbose_name='Автопродление'),
        ),
    ]
