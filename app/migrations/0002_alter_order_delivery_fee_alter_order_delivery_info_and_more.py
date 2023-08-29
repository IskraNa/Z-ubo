# Generated by Django 4.2.1 on 2023-08-24 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_fee',
            field=models.IntegerField(default=120),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.deliveryinfo'),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.CharField(auto_created=True, blank=True, max_length=50, primary_key=True, serialize=False),
        ),
    ]