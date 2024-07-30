from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0004_normalize_store"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- Insert distinct product data into the new Product table
                INSERT INTO product (product_id, unit_price, product_category, product_type, product_detail)
                SELECT DISTINCT ON (product_id) 
                    product_id, 
                    COALESCE(unit_price, 0),  -- Replace null unit_price with a default value
                    product_category, 
                    product_type, 
                    product_detail
                FROM raw_transaction;

                -- Reset the product_id sequence
                SELECT setval(pg_get_serial_sequence('product', 'product_id'), coalesce(max(product_id), 1), max(product_id) IS NOT NULL) FROM product;
            """,
            reverse_sql="""
                -- Truncate the product table (reverse operation)
                TRUNCATE TABLE product RESTART IDENTITY CASCADE;
            """,
        ),
    ]
