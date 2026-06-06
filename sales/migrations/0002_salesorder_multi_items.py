from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        # Make product_name/quantity/unit_price nullable for multi-item orders
        migrations.AlterField(
            model_name='salesorder',
            name='product_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12),
        ),
        # Add new order-level fields
        migrations.AddField(
            model_name='salesorder',
            name='customer_id',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='priority',
            field=models.CharField(
                choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')],
                default='medium',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='shipping_address',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
        # Create the OrderItem model
        migrations.CreateModel(
            name='SalesOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('order', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='items',
                    to='sales.salesorder',
                )),
            ],
        ),
    ]
