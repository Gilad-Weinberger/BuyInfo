# Generated by Django 4.1.12 on 2023-10-22 13:01

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='expenses',
            field=jsonfield.fields.JSONField(null=True),
        ),
    ]
