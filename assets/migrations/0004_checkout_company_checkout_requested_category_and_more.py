import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_company_user_company_companymembershiprequest'),
        ('assets', '0003_alter_device_asset_tag_alter_device_serial_number'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checkouts', to='accounts.company'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='requested_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requested_checkouts', to='assets.category'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='requested_device_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Requested Device / Model'),
        ),
        migrations.AddField(
            model_name='device',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='accounts.company'),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='checkouts', to='assets.device'),
        ),
        migrations.AddIndex(
            model_name='checkout',
            index=models.Index(fields=['company'], name='assets_chec_company_d6b81a_idx'),
        ),
        migrations.AddIndex(
            model_name='device',
            index=models.Index(fields=['company'], name='assets_devi_company_34428f_idx'),
        ),
    ]
