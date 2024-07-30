# api.py
from typing import List

from django.db import connection
from ninja import NinjaAPI

api = NinjaAPI()


@api.post("/store/")
def create_store(request, store_location: str):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM create_store(%s);", [store_location])
        result = cursor.fetchone()
        return {"store_id": result[0], "store_location": result[1]}


@api.put("/store/{store_id}/")
def modify_store(request, store_id: int, store_location: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM modify_store(%s, %s);", [store_id, store_location]
        )
        result = cursor.fetchone()
        return {"store_id": result[0], "store_location": result[1]}


@api.delete("/store/{store_id}/")
def delete_store(request, store_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT delete_store(%s);", [store_id])
    return {"success": True}


@api.get("/store/", response=List[dict])
def list_stores(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM list_stores();")
        result = cursor.fetchall()
        return [{"store_id": row[0], "store_location": row[1]} for row in result]


@api.post("/product/")
def create_product(
    request,
    unit_price: float,
    product_category: str,
    product_type: str,
    product_detail: str,
):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM create_product(%s, %s, %s, %s);",
            [unit_price, product_category, product_type, product_detail],
        )
        result = cursor.fetchone()
        return {
            "product_id": result[0],
            "unit_price": result[1],
            "product_category": result[2],
            "product_type": result[3],
            "product_detail": result[4],
        }


@api.put("/product/{product_id}/")
def modify_product(
    request,
    product_id: int,
    unit_price: float,
    product_category: str,
    product_type: str,
    product_detail: str,
):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM modify_product(%s, %s, %s, %s, %s);",
            [product_id, unit_price, product_category, product_type, product_detail],
        )
        result = cursor.fetchone()
        return {
            "product_id": result[0],
            "unit_price": result[1],
            "product_category": result[2],
            "product_type": result[3],
            "product_detail": result[4],
        }


@api.delete("/product/{product_id}/")
def delete_product(request, product_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT delete_product(%s);", [product_id])
    return {"success": True}


@api.get("/product/", response=List[dict])
def list_products(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM list_products();")
        result = cursor.fetchall()
        return [
            {
                "product_id": row[0],
                "unit_price": row[1],
                "product_category": row[2],
                "product_type": row[3],
                "product_detail": row[4],
            }
            for row in result
        ]


@api.post("/transaction/")
def create_transaction(
    request,
    transaction_date: str,
    transaction_time: str,
    transaction_qty: int,
    store_id: int,
    product_id: int,
):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM create_transaction(%s, %s, %s, %s, %s);",
            [transaction_date, transaction_time, transaction_qty, store_id, product_id],
        )
        result = cursor.fetchone()
        return {
            "transaction_id": result[0],
            "transaction_date": result[1],
            "transaction_time": result[2],
            "transaction_qty": result[3],
            "store_id": result[4],
            "product_id": result[5],
        }


@api.put("/transaction/{transaction_id}/")
def modify_transaction(
    request,
    transaction_id: int,
    transaction_date: str,
    transaction_time: str,
    transaction_qty: int,
    store_id: int,
    product_id: int,
):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM modify_transaction(%s, %s, %s, %s, %s, %s);",
            [
                transaction_id,
                transaction_date,
                transaction_time,
                transaction_qty,
                store_id,
                product_id,
            ],
        )
        result = cursor.fetchone()
        return {
            "transaction_id": result[0],
            "transaction_date": result[1],
            "transaction_time": result[2],
            "transaction_qty": result[3],
            "store_id": result[4],
            "product_id": result[5],
        }


@api.delete("/transaction/{transaction_id}/")
def delete_transaction(request, transaction_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT delete_transaction(%s);", [transaction_id])
    return {"success": True}


@api.get("/transaction/", response=List[dict])
def list_transactions(request, limit: int = 10, offset: int = 0):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM list_transactions(%s, %s);", [limit, offset])
        result = cursor.fetchall()
        return [
            {
                "transaction_id": row[0],
                "transaction_date": row[1],
                "transaction_time": row[2],
                "transaction_qty": row[3],
                "store_id": row[4],
                "product_id": row[5],
            }
            for row in result
        ]
