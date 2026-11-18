
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('is_custom', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SystemSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('self_checkout_allowed', models.BooleanField(default=False)),
                ('overdue_days', models.PositiveIntegerField(default=7)),
                ('field_purchase_date_enabled', models.BooleanField(default=True)),
                ('field_brand_enabled', models.BooleanField(default=True)),
                ('field_location_enabled', models.BooleanField(default=False)),
                ('field_notes_enabled', models.BooleanField(default=True)),
                ('field_warranty_expiry_enabled', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'System Settings',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_tag', models.CharField(max_length=50, unique=True)),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('model_name', models.CharField(max_length=150, verbose_name='Model')),
                ('custom_category_label', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('available', 'Available'), ('borrowed', 'Borrowed'), ('repair', 'Under Repair')], default='available', max_length=20)),
                ('brand', models.CharField(blank=True, max_length=100)),
                ('purchase_date', models.DateField(blank=True, null=True)),
                ('warranty_expiry', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=150)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='devices', to='assets.category')),
            ],
            options={
                'ordering': ['asset_tag'],
            },
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending Approval'), ('active', 'Active'), ('returned', 'Returned'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('checked_out_at', models.DateTimeField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('returned_at', models.DateTimeField(blank=True, null=True)),
                ('purpose', models.CharField(blank=True, max_length=255)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_checkouts', to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='checkouts', to=settings.AUTH_USER_MODEL)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='checkouts', to='assets.device')),
            ],
            options={
                'ordering': ['-requested_at'],
            },
        ),
        migrations.CreateModel(
            name='MaintenanceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='maintenance_photos/')),
                ('is_resolved', models.BooleanField(default=False)),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_logs', to='assets.device')),
                ('reported_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reported_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-reported_at'],
            },
        ),
        migrations.AddIndex(
            model_name='device',
            index=models.Index(fields=['status'], name='assets_devi_status_03b2ce_idx'),
        ),
        migrations.AddIndex(
            model_name='device',
            index=models.Index(fields=['category'], name='assets_devi_categor_4f676d_idx'),
        ),
        migrations.AddIndex(
            model_name='checkout',
            index=models.Index(fields=['status'], name='assets_chec_status_8b835e_idx'),
        ),
        migrations.AddIndex(
            model_name='checkout',
            index=models.Index(fields=['employee', 'status'], name='assets_chec_employe_cffc2b_idx'),
        ),
    ]
