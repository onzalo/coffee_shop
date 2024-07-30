from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0002_seed_initial_data"),
    ]

    operations = [
        migrations.RunSQL(
            """
            -- Create the product table
            CREATE TABLE product (
                product_id SERIAL PRIMARY KEY,
                unit_price FLOAT NOT NULL,
                product_category VARCHAR(255) NOT NULL,
                product_type VARCHAR(255) NOT NULL,
                product_detail VARCHAR(255) NOT NULL
            );

            -- Create the store table
            CREATE TABLE store (
                store_id SERIAL PRIMARY KEY,
                store_location VARCHAR(255) NOT NULL
            );

            -- Create the transaction table
            CREATE TABLE transaction (
                transaction_id BIGSERIAL PRIMARY KEY,
                transaction_date DATE NOT NULL,
                transaction_time TIME NOT NULL,
                transaction_qty INTEGER NOT NULL,
                unit_price FLOAT NOT NULL,
                product_id INTEGER NOT NULL,
                store_id INTEGER NOT NULL,
                FOREIGN KEY (product_id) REFERENCES product (product_id) ON DELETE CASCADE,
                FOREIGN KEY (store_id) REFERENCES store (store_id) ON DELETE CASCADE
            );
            """,
            reverse_sql="""
            DROP TABLE IF EXISTS transaction;
            DROP TABLE IF EXISTS product;
            DROP TABLE IF EXISTS store;
            """,
        ),
    ]
