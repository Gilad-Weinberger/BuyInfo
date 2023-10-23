# Generated by Django 4.1.12 on 2023-10-23 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_expense_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.expense_type'),
        ),
    ]