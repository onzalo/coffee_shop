from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE raw_transaction (
                transaction_id BIGSERIAL PRIMARY KEY,
                transaction_date DATE NOT NULL,
                transaction_time TIME NOT NULL,
                transaction_qty INTEGER NOT NULL,
                store_id INTEGER NOT NULL,
                store_location VARCHAR(255) NOT NULL,
                product_id INTEGER NOT NULL,
                unit_price FLOAT NOT NULL,
                product_category VARCHAR(255) NOT NULL,
                product_type VARCHAR(255) NOT NULL,
                product_detail VARCHAR(255) NOT NULL
            );
            """,
            reverse_sql="DROP TABLE raw_transaction;",
        ),
    ]
