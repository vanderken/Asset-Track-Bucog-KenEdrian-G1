
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_remove_device_custom_category_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='asset_tag',
            field=models.CharField(max_length=50, unique=True, verbose_name='Asset Tag'),
        ),
        migrations.AlterField(
            model_name='device',
            name='serial_number',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Serial Number'),
        ),
    ]
