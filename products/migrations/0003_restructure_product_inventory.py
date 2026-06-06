from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_rename_price_product_retail_price_and_more'),
    ]

    operations = [
        # Rename retail_price → unit_price
        migrations.RenameField(
            model_name='product',
            old_name='retail_price',
            new_name='unit_price',
        ),
        # Rename stock_quantity → stock
        migrations.RenameField(
            model_name='product',
            old_name='stock_quantity',
            new_name='stock',
        ),
        # Remove wholesale_price
        migrations.RemoveField(
            model_name='product',
            name='wholesale_price',
        ),
        # Add new fields
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='reorder_level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='last_restocked',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='product',
            name='batch_number',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='expiry_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
