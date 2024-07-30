import pandas as pd
from django.db import connection, migrations


def load_xlsx_data(apps, schema_editor):
    # Define the path to your Excel file
    df = pd.read_excel("dataset/coffee_shop_sales.xlsx")

    # Prepare the data for bulk insert
    data = [
        (
            row["transaction_date"],
            row["transaction_time"],
            row["transaction_qty"],
            row["store_id"],
            row["store_location"],
            row["product_id"],
            row["unit_price"],
            row["product_category"],
            row["product_type"],
            row["product_detail"],
        )
        for _, row in df.iterrows()
    ]

    # Bulk insert the data using raw SQL
    with connection.cursor() as cursor:
        cursor.executemany(
            """
            INSERT INTO raw_transaction (
                transaction_date,
                transaction_time,
                transaction_qty,
                store_id,
                store_location,
                product_id,
                unit_price,
                product_category,
                product_type,
                product_detail
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            data,
        )


def delete_table_data(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM raw_transaction")


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_xlsx_data, reverse_code=delete_table_data),
    ]
