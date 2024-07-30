from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0006_normalize_transaction"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- Create a stored procedure to add a store and return the created store
                CREATE OR REPLACE FUNCTION create_store(new_store_location VARCHAR(255)) 
                RETURNS TABLE(store_id INTEGER, store_location VARCHAR(255)) 
                AS $$
                DECLARE
                    result RECORD;
                BEGIN
                    INSERT INTO store (store_location)
                    VALUES (new_store_location)
                    RETURNING store.store_id, store.store_location INTO result;
                    RETURN QUERY SELECT result.store_id, result.store_location;
                END;
                $$ LANGUAGE plpgsql;

                -- Create a stored procedure to modify a store and return the modified store
                CREATE OR REPLACE FUNCTION modify_store(p_store_id INTEGER, new_store_location VARCHAR(255)) 
                RETURNS TABLE(store_id INTEGER, store_location VARCHAR(255)) 
                AS $$
                DECLARE
                    result RECORD;
                BEGIN
                    UPDATE store
                    SET store_location = new_store_location
                    WHERE store.store_id = p_store_id
                    RETURNING store.store_id, store.store_location INTO result;
                    RETURN QUERY SELECT result.store_id, result.store_location;
                END;
                $$ LANGUAGE plpgsql;

                -- Create a stored procedure to delete a store
                CREATE OR REPLACE FUNCTION delete_store(p_store_id INTEGER) 
                RETURNS VOID 
                AS $$
                BEGIN
                    DELETE FROM store
                    WHERE store.store_id = p_store_id;
                END;
                $$ LANGUAGE plpgsql;

                -- Create a stored procedure to list stores
                CREATE OR REPLACE FUNCTION list_stores() 
                RETURNS TABLE(store_id INTEGER, store_location VARCHAR(255)) 
                AS $$
                BEGIN
                    RETURN QUERY 
                    SELECT store.store_id, store.store_location 
                    FROM store 
                    ORDER BY store.store_id ASC;
                END;
                $$ LANGUAGE plpgsql;
            """,
            reverse_sql="""
                -- Drop the stored procedure to add a store
                DROP FUNCTION IF EXISTS create_store(VARCHAR);

                -- Drop the stored procedure to modify a store
                DROP FUNCTION IF EXISTS modify_store(INTEGER, VARCHAR);

                -- Drop the stored procedure to delete a store
                DROP FUNCTION IF EXISTS delete_store(INTEGER);

                -- Drop the stored procedure to list stores
                DROP FUNCTION IF EXISTS list_stores();
            """,
        ),
    ]
