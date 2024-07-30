from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0007_store_operations"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- Create a stored procedure to add a product and return the created product
                CREATE OR REPLACE FUNCTION create_product(new_unit_price FLOAT, new_product_category VARCHAR(255), new_product_type VARCHAR(255), new_product_detail VARCHAR(255)) 
                RETURNS TABLE(product_id INTEGER, unit_price FLOAT, product_category VARCHAR(255), product_type VARCHAR(255), product_detail VARCHAR(255)) 
                AS $$
                DECLARE
                    result RECORD;
                BEGIN
                    INSERT INTO product (unit_price, product_category, product_type, product_detail)
                    VALUES (new_unit_price, new_product_category, new_product_type, new_product_detail)
                    RETURNING product.product_id, product.unit_price, product.product_category, product.product_type, product.product_detail INTO result;
                    RETURN QUERY SELECT result.product_id, result.unit_price, result.product_category, result.product_type, result.product_detail;
                END;
                $$ LANGUAGE plpgsql;

                -- Create a stored procedure to modify a product and return the modified product
                CREATE OR REPLACE FUNCTION modify_product(p_product_id INTEGER, new_unit_price FLOAT, new_product_category VARCHAR(255), new_product_type VARCHAR(255), new_product_detail VARCHAR(255)) 
                RETURNS TABLE(product_id INTEGER, unit_price FLOAT, product_category VARCHAR(255), product_type VARCHAR(255), product_detail VARCHAR(255)) 
                AS $$
                DECLARE
                    result RECORD;
                BEGIN
                    UPDATE product
                    SET unit_price = new_unit_price,
                        product_category = new_product_category,
                        product_type = new_product_type,
                        product_detail = new_product_detail
                    WHERE product.product_id = p_product_id
                    RETURNING product.product_id, product.unit_price, product.product_category, product.product_type, product.product_detail INTO result;
                    RETURN QUERY SELECT result.product_id, result.unit_price, result.product_category, result.product_type, result.product_detail;
                END;
                $$ LANGUAGE plpgsql;

                -- Create a stored procedure to delete a product
                CREATE OR REPLACE FUNCTION delete_product(p_product_id INTEGER) 
                RETURNS VOID 
                AS $$
                BEGIN
                    DELETE FROM product
                    WHERE product.product_id = p_product_id;
                END;
                $$ LANGUAGE plpgsql;

                -- Create a stored procedure to list products
                CREATE OR REPLACE FUNCTION list_products() 
                RETURNS TABLE(product_id INTEGER, unit_price FLOAT, product_category VARCHAR(255), product_type VARCHAR(255), product_detail VARCHAR(255)) 
                AS $$
                BEGIN
                    RETURN QUERY 
                    SELECT product.product_id, product.unit_price, product.product_category, product.product_type, product.product_detail 
                    FROM product 
                    ORDER BY product.product_id ASC;
                END;
                $$ LANGUAGE plpgsql;
            """,
            reverse_sql="""
                -- Drop the stored procedure to add a product
                DROP FUNCTION IF EXISTS create_product(FLOAT, VARCHAR, VARCHAR, VARCHAR);

                -- Drop the stored procedure to modify a product
                DROP FUNCTION IF EXISTS modify_product(INTEGER, FLOAT, VARCHAR, VARCHAR, VARCHAR);

                -- Drop the stored procedure to delete a product
                DROP FUNCTION IF EXISTS delete_product(INTEGER);

                -- Drop the stored procedure to list products
                DROP FUNCTION IF EXISTS list_products();
            """,
        ),
    ]
