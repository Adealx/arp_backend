import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Transforms SalesOrder/SalesOrderItem from the 0001-0003 schema to the
    current model layout.  Written to be idempotent so it is safe to run
    against a DB that already has the target schema (e.g. after a --fake
    mis-fire left this migration marked as un-applied).
    """

    dependencies = [
        ('customers', '0003_add_status_field'),
        ('products', '0003_restructure_product_inventory'),
        ('sales', '0003_add_approved_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Truncate only when the old schema is still present.
        migrations.RunSQL(
            sql="""
                DO $$ BEGIN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'sales_salesorder'
                          AND column_name  = 'customer_name'
                    ) THEN
                        TRUNCATE TABLE sales_salesorder RESTART IDENTITY CASCADE;
                    END IF;
                END $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),

        # Drop old SalesOrderItem only if it still has the old VARCHAR product_name
        # column (i.e. not yet migrated to the product FK structure).
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        DO $$ BEGIN
                            IF EXISTS (
                                SELECT 1 FROM information_schema.tables
                                WHERE table_name = 'sales_salesorderitem'
                            ) AND NOT EXISTS (
                                SELECT 1 FROM information_schema.columns
                                WHERE table_name = 'sales_salesorderitem'
                                  AND column_name  = 'product_id'
                            ) THEN
                                DROP TABLE sales_salesorderitem CASCADE;
                            END IF;
                        END $$;
                    """,
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[migrations.DeleteModel(name='SalesOrderItem')],
        ),

        # Remove the old VARCHAR customer_id field (added in 0002).
        # Skip if already gone or already replaced by the integer FK column.
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        DO $$ BEGIN
                            IF EXISTS (
                                SELECT 1 FROM information_schema.columns
                                WHERE table_name = 'sales_salesorder'
                                  AND column_name  = 'customer_id'
                                  AND data_type    = 'character varying'
                            ) THEN
                                ALTER TABLE sales_salesorder DROP COLUMN customer_id;
                            END IF;
                        END $$;
                    """,
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[migrations.RemoveField(model_name='salesorder', name='customer_id')],
        ),

        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    "ALTER TABLE sales_salesorder DROP COLUMN IF EXISTS customer_name;",
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[migrations.RemoveField(model_name='salesorder', name='customer_name')],
        ),

        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    "ALTER TABLE sales_salesorder DROP COLUMN IF EXISTS product_name;",
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[migrations.RemoveField(model_name='salesorder', name='product_name')],
        ),

        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    "ALTER TABLE sales_salesorder DROP COLUMN IF EXISTS quantity;",
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[migrations.RemoveField(model_name='salesorder', name='quantity')],
        ),

        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    "ALTER TABLE sales_salesorder DROP COLUMN IF EXISTS unit_price;",
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[migrations.RemoveField(model_name='salesorder', name='unit_price')],
        ),

        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    "ALTER TABLE sales_salesorder DROP COLUMN IF EXISTS priority;",
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[migrations.RemoveField(model_name='salesorder', name='priority')],
        ),

        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    "ALTER TABLE sales_salesorder DROP COLUMN IF EXISTS due_date;",
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[migrations.RemoveField(model_name='salesorder', name='due_date')],
        ),

        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    "ALTER TABLE sales_salesorder DROP COLUMN IF EXISTS shipping_address;",
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[migrations.RemoveField(model_name='salesorder', name='shipping_address')],
        ),

        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    "ALTER TABLE sales_salesorder DROP COLUMN IF EXISTS notes;",
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[migrations.RemoveField(model_name='salesorder', name='notes')],
        ),

        # Add the customer FK column only if it doesn't exist yet.
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        DO $$ BEGIN
                            IF NOT EXISTS (
                                SELECT 1 FROM information_schema.columns
                                WHERE table_name = 'sales_salesorder'
                                  AND column_name  = 'customer_id'
                            ) THEN
                                ALTER TABLE sales_salesorder
                                    ADD COLUMN customer_id BIGINT NOT NULL DEFAULT 0
                                    REFERENCES customers_customer(id) ON DELETE CASCADE;
                            END IF;
                        END $$;
                    """,
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='salesorder',
                    name='customer',
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='sales_orders',
                        to='customers.customer',
                    ),
                ),
            ],
        ),

        migrations.AlterField(
            model_name='salesorder',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),

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

        # Recreate SalesOrderItem with proper FK to Product and line_total.
        # IF NOT EXISTS makes this safe to re-run.
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        CREATE TABLE IF NOT EXISTS sales_salesorderitem (
                            id         BIGSERIAL PRIMARY KEY,
                            quantity   INTEGER      NOT NULL CHECK (quantity > 0),
                            unit_price NUMERIC(12,2) NOT NULL,
                            line_total NUMERIC(12,2) NOT NULL DEFAULT 0,
                            order_id   BIGINT NOT NULL
                                REFERENCES sales_salesorder(id) ON DELETE CASCADE,
                            product_id BIGINT NOT NULL
                                REFERENCES products_product(id) ON DELETE CASCADE
                        );
                    """,
                    reverse_sql="DROP TABLE IF EXISTS sales_salesorderitem;",
                ),
            ],
            state_operations=[
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
            ],
        ),
    ]
