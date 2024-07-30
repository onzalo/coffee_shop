from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0005_normalize_product"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- Insert transaction data into the new Transaction table
                INSERT INTO transaction (transaction_id, unit_price, transaction_date, transaction_time, transaction_qty, store_id, product_id)
                SELECT 
                    transaction_id, 
                    COALESCE(unit_price, 0),  -- Replace null unit_price with a default value
                    transaction_date, 
                    transaction_time, 
                    transaction_qty, 
                    store_id, 
                    product_id
                FROM raw_transaction
                WHERE unit_price IS NOT NULL;  -- Ensure all required columns are filled

                -- Reset the transaction_id sequence
                SELECT setval(pg_get_serial_sequence('transaction', 'transaction_id'), coalesce(max(transaction_id), 1), max(transaction_id) IS NOT NULL) FROM transaction;
            """,
            reverse_sql="""
                -- Truncate the transaction table (reverse operation)
                TRUNCATE TABLE transaction RESTART IDENTITY CASCADE;
            """,
        ),
    ]
