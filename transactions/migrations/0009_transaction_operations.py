from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0008_product_operations"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- Create a stored procedure to add a transaction and return the created transaction
                CREATE OR REPLACE FUNCTION create_transaction(new_transaction_date DATE, new_transaction_time TIME, new_transaction_qty INTEGER, new_store_id INTEGER, new_product_id INTEGER) 
                RETURNS TABLE(transaction_id BIGINT, transaction_date DATE, transaction_time TIME, transaction_qty INTEGER, store_id INTEGER, product_id INTEGER) 
                AS $$
                DECLARE
                    result RECORD;
                BEGIN
                    INSERT INTO transaction (transaction_date, transaction_time, transaction_qty, store_id, product_id)
                    VALUES (new_transaction_date, new_transaction_time, new_transaction_qty, new_store_id, new_product_id)
                    RETURNING transaction.transaction_id, transaction.transaction_date, transaction.transaction_time, transaction.transaction_qty, transaction.store_id, transaction.product_id INTO result;
                    RETURN QUERY SELECT result.transaction_id, result.transaction_date, result.transaction_time, result.transaction_qty, result.store_id, result.product_id;
                END;
                $$ LANGUAGE plpgsql;

                -- Create a stored procedure to modify a transaction and return the modified transaction
                CREATE OR REPLACE FUNCTION modify_transaction(p_transaction_id BIGINT, new_transaction_date DATE, new_transaction_time TIME, new_transaction_qty INTEGER, new_store_id INTEGER, new_product_id INTEGER) 
                RETURNS TABLE(transaction_id BIGINT, transaction_date DATE, transaction_time TIME, transaction_qty INTEGER, store_id INTEGER, product_id INTEGER) 
                AS $$
                DECLARE
                    result RECORD;
                BEGIN
                    UPDATE transaction
                    SET transaction_date = new_transaction_date,
                        transaction_time = new_transaction_time,
                        transaction_qty = new_transaction_qty,
                        store_id = new_store_id,
                        product_id = new_product_id
                    WHERE transaction.transaction_id = p_transaction_id
                    RETURNING transaction.transaction_id, transaction.transaction_date, transaction.transaction_time, transaction_qty, store_id, product_id INTO result;
                    RETURN QUERY SELECT result.transaction_id, result.transaction_date, result.transaction_time, result.transaction_qty, result.store_id, result.product_id;
                END;
                $$ LANGUAGE plpgsql;

                -- Create a stored procedure to delete a transaction
                CREATE OR REPLACE FUNCTION delete_transaction(p_transaction_id BIGINT) 
                RETURNS VOID 
                AS $$
                BEGIN
                    DELETE FROM transaction
                    WHERE transaction.transaction_id = p_transaction_id;
                END;
                $$ LANGUAGE plpgsql;

                -- Create a stored procedure to list transactions
                CREATE OR REPLACE FUNCTION list_transactions() 
                RETURNS TABLE(transaction_id BIGINT, transaction_date DATE, transaction_time TIME, transaction_qty INTEGER, store_id INTEGER, product_id INTEGER) 
                AS $$
                BEGIN
                    RETURN QUERY 
                    SELECT transaction.transaction_id, transaction.transaction_date, transaction.transaction_time, transaction.transaction_qty, transaction.store_id, transaction.product_id 
                    FROM transaction 
                    ORDER BY transaction.transaction_id ASC;
                END;
                $$ LANGUAGE plpgsql;
            """,
            reverse_sql="""
                -- Drop the stored procedure to add a transaction
                DROP FUNCTION IF EXISTS create_transaction(DATE, TIME, INTEGER, INTEGER, INTEGER);

                -- Drop the stored procedure to modify a transaction
                DROP FUNCTION IF EXISTS modify_transaction(BIGINT, DATE, TIME, INTEGER, INTEGER, INTEGER);

                -- Drop the stored procedure to delete a transaction
                DROP FUNCTION IF EXISTS delete_transaction(BIGINT);

                -- Drop the stored procedure to list transactions
                DROP FUNCTION IF EXISTS list_transactions();
            """,
        ),
    ]
