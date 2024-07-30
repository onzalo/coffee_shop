from django.db import models


class RawTransaction(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    transaction_date = models.DateField()
    transaction_time = models.TimeField(max_length=255)
    transaction_qty = models.IntegerField()
    store_id = models.IntegerField()
    store_location = models.CharField(max_length=255)
    product_id = models.IntegerField()
    unit_price = models.FloatField()
    product_category = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    product_detail = models.CharField(max_length=255)

    class Meta:
        db_table = "raw_transaction"
        app_label = "transactions"


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_location = models.CharField(max_length=255)

    class Meta:
        db_table = "store"
        app_label = "transactions"


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    unit_price = models.FloatField()
    product_category = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    product_detail = models.CharField(max_length=255)

    class Meta:
        db_table = "product"
        app_label = "transactions"


class Transaction(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    transaction_date = models.DateField()
    transaction_time = models.TimeField(max_length=255)
    transaction_qty = models.IntegerField()
    unit_price = models.FloatField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "transaction"
        app_label = "transactions"
