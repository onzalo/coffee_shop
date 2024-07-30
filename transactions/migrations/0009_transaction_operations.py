from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0008_product_operations"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- Create a stored procedure to list transactions with limit and offset
                CREATE OR REPLACE FUNCTION list_transactions(p_limit INT, p_offset INT) 
                RETURNS TABLE(transaction_id BIGINT, transaction_date DATE, transaction_time TIME, transaction_qty INTEGER, store_id INTEGER, product_id INTEGER) 
                AS $$
                BEGIN
                    RETURN QUERY 
                    SELECT transaction.transaction_id, transaction.transaction_date, transaction.transaction_time, transaction.transaction_qty, transaction.store_id, transaction.product_id 
                    FROM transaction 
                    ORDER BY transaction.transaction_id DESC
                    LIMIT p_limit OFFSET p_offset;
                END;
                $$ LANGUAGE plpgsql;
            """,
            reverse_sql="""
                -- Drop the stored procedure to list transactions
                DROP FUNCTION IF EXISTS list_transactions(INT, INT);
            """,
        ),
    ]
