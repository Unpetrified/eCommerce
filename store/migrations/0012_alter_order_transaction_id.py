# Generated by Django 3.2.5 on 2023-01-28 20:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_shipping_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]