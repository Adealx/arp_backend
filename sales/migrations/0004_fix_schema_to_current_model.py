import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Replaces the two conflicting branches that both tried to restructure
    SalesOrder after 0002_salesorder_multi_items was applied.

    DB state coming in (0001_initial + 0002_salesorder_multi_items + 0003_add_approved_status):
      sales_salesorder has: customer_name, product_name, quantity, unit_price,
        customer_id (VARCHAR), priority, due_date, shipping_address, notes
      sales_salesorderitem has: product_name (VARCHAR), quantity, unit_price

    DB state going out (matches current models.py):
      sales_salesorder has: sales_rep FK, customer FK, total_amount, status, timestamps
      sales_salesorderitem has: order FK, product FK, quantity, unit_price, line_total
    """

    dependencies = [
        ('customers', '0003_add_status_field'),
        ('products', '0003_restructure_product_inventory'),
        ('sales', '0003_add_approved_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Clear all sales data before restructuring — there is no real production
        # data here; the old schema is incompatible and rows cannot be migrated.
        # CASCADE handles the old sales_salesorderitem rows automatically.
        migrations.RunSQL(
            "TRUNCATE TABLE sales_salesorder RESTART IDENTITY CASCADE;",
            reverse_sql=migrations.RunSQL.noop,
        ),

        # Drop the old SalesOrderItem (wrong structure — product_name CharField, no line_total)
        migrations.DeleteModel(name='SalesOrderItem'),

        # Remove the VARCHAR customer_id field (from 0002_salesorder_multi_items)
        migrations.RemoveField(model_name='salesorder', name='customer_id'),

        # Remove obsolete flat fields from 0001_initial / 0002_salesorder_multi_items
        migrations.RemoveField(model_name='salesorder', name='customer_name'),
        migrations.RemoveField(model_name='salesorder', name='product_name'),
        migrations.RemoveField(model_name='salesorder', name='quantity'),
        migrations.RemoveField(model_name='salesorder', name='unit_price'),
        migrations.RemoveField(model_name='salesorder', name='priority'),
        migrations.RemoveField(model_name='salesorder', name='due_date'),
        migrations.RemoveField(model_name='salesorder', name='shipping_address'),
        migrations.RemoveField(model_name='salesorder', name='notes'),

        # Add FK to Customer (creates customer_id INTEGER column)
        migrations.AddField(
            model_name='salesorder',
            name='customer',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='sales_orders',
                to='customers.customer',
            ),
        ),

        # Fix total_amount to be non-nullable with default 0
        migrations.AlterField(
            model_name='salesorder',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),

        # Update status choices to final set
        migrations.AlterField(
            model_name='salesorder',
            name='status',
            field=models.CharField(
                choices=[
                    ('Pending', 'Pending'),
                    ('Approved', 'Approved'),
                    ('Rejected', 'Rejected'),
                    ('Invoiced', 'Invoiced'),
                ],
                default='Pending',
                max_length=20,
            ),
        ),

        # Recreate SalesOrderItem with proper FK to Product and line_total
        migrations.CreateModel(
            name='SalesOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('line_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('order', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='items',
                    to='sales.salesorder',
                )),
                ('product', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='order_items',
                    to='products.product',
                )),
            ],
        ),
    ]
