# Generated by Django 4.1.12 on 2023-10-29 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0003_alter_receipt_shop_alter_receipt_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receiptproduct',
            name='shop',
        ),
    ]
