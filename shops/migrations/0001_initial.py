# Generated by Django 4.1.12 on 2023-10-26 12:00

from django.db import migrations, models
import django.db.models.deletion
import shops.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement_unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=150)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=50)),
                ('unit_of_measurement_price', models.DecimalField(decimal_places=4, max_digits=50)),
                ('measurement_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.measurement_unit')),
            ],
        ),
        migrations.CreateModel(
            name='Recipet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=shops.models.recipet_image_upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='Shops_net',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to=shops.models.shops_net_logo_upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='Unit_of_measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.measurement_unit')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('shop_id', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100, null=True)),
                ('shops_net', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.shops_net')),
            ],
        ),
        migrations.CreateModel(
            name='RecipetProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.product')),
                ('recipet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.recipet')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='shops_net',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.shops_net'),
        ),
        migrations.AddField(
            model_name='product',
            name='unit_of_measurement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.unit_of_measurement'),
        ),
    ]
