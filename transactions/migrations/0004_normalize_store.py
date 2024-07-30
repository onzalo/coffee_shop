from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("transactions", "0003_normalize_data"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- Insert distinct store data into the new Store table
                INSERT INTO store (store_id, store_location)
                SELECT DISTINCT ON (store_id) 
                    store_id, 
                    store_location
                FROM raw_transaction;

                -- Reset the store_id sequence
                SELECT setval(pg_get_serial_sequence('store', 'store_id'), coalesce(max(store_id), 1), max(store_id) IS NOT NULL) FROM store;
            """,
            reverse_sql="""
                -- Truncate the store table (reverse operation)
                TRUNCATE TABLE store RESTART IDENTITY CASCADE;
            """,
        ),
    ]
